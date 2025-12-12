import asyncio
import codecs
import os
import platform
import shutil
import signal
from collections.abc import AsyncGenerator, Callable
from typing import Any

from exponent.core.remote_execution.default_env import get_process_env
from exponent.core.remote_execution.languages.types import (
    ShellExecutionResult,
    StreamedOutputPiece,
)

STDOUT_FD = 1
STDERR_FD = 2
MAX_TIMEOUT = 300


def get_rc_file_source_command(shell_path: str) -> str:
    """
    Returns a command to source the user's shell rc file
    Login profiles are already sourced via the -l flag
    """
    # On Windows, shell behavior is different
    if platform.system() == "Windows":
        return ""  # Windows shells don't typically use rc files in the same way

    shell_name = os.path.basename(shell_path)
    home_dir = os.path.expanduser("~")

    if shell_name == "zsh":
        zshrc = os.path.join(home_dir, ".zshrc")
        if os.path.exists(zshrc):
            return f"source {zshrc} 2>/dev/null || true; "
    elif shell_name == "bash":
        bashrc = os.path.join(home_dir, ".bashrc")
        if os.path.exists(bashrc):
            return f"source {bashrc} 2>/dev/null || true; "

    return ""  # No rc file found or unsupported shell


async def read_stream(
    stream: asyncio.StreamReader, fd: int, output: list[tuple[int, str]]
) -> AsyncGenerator[StreamedOutputPiece, None]:
    # Use an incremental decoder to properly handle multi-byte UTF-8 sequences
    # that may be split across read boundaries
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

    while True:
        try:
            data = await stream.read(50_000)
            if not data:
                # Flush any remaining bytes in decoder
                chunk = decoder.decode(b"", final=True)
                if chunk:
                    output.append((fd, chunk))
                    yield StreamedOutputPiece(content=chunk)
                break
            chunk = decoder.decode(data, final=False)
            if chunk:
                output.append((fd, chunk))
                yield StreamedOutputPiece(content=chunk)
        except asyncio.CancelledError:
            raise
        except Exception:
            break


async def execute_shell_streaming(  # noqa: PLR0915
    code: str,
    working_directory: str,
    timeout: int,
    should_halt: Callable[[], bool] | None = None,
    env: dict[str, str] | None = None,
) -> AsyncGenerator[StreamedOutputPiece | ShellExecutionResult, None]:
    timeout_seconds = min(timeout, MAX_TIMEOUT)

    shell_path = os.environ.get("SHELL") or shutil.which("bash") or shutil.which("sh")

    # Track whether we created a process group (for proper cleanup)
    uses_process_group = False

    if not shell_path:
        process = await asyncio.create_subprocess_shell(
            code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_directory,
            env=get_process_env(env),
        )
    else:
        # Add rc file sourcing to the command
        rc_source_cmd = get_rc_file_source_command(shell_path)
        full_command = f"{rc_source_cmd}{code}"

        process = await asyncio.create_subprocess_exec(
            shell_path,
            "-l",
            "-c",
            full_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_directory,
            env=get_process_env(env),
            start_new_session=True if platform.system() != "Windows" else False,
        )
        uses_process_group = platform.system() != "Windows"

    exit_code = None
    output: list[tuple[int, str]] = []
    halted = False
    timed_out = False
    assert process.stdout
    assert process.stderr

    async def monitor_halt() -> None:
        nonlocal halted

        while True:
            if should_halt and should_halt():
                # Send signal to process group for proper interrupt propagation
                try:
                    if uses_process_group:
                        # Send SIGTERM to the process group
                        try:
                            os.killpg(process.pid, signal.SIGTERM)
                        except OSError:
                            # Fallback if not a process group leader
                            process.terminate()
                        try:
                            await asyncio.wait_for(process.wait(), timeout=2.0)
                        except TimeoutError:
                            # Fall back to SIGKILL
                            try:
                                os.killpg(process.pid, signal.SIGKILL)
                            except OSError:
                                process.kill()
                    else:
                        # No process group - use regular terminate/kill
                        process.terminate()
                        try:
                            await asyncio.wait_for(process.wait(), timeout=2.0)
                        except TimeoutError:
                            process.kill()
                except ProcessLookupError:
                    # Process already terminated
                    pass
                halted = True
                break
            if process.returncode is not None:
                break
            await asyncio.sleep(0.1)

    def on_timeout() -> None:
        nonlocal timed_out
        timed_out = True
        try:
            if uses_process_group:
                # Kill the entire process group, not just the shell process
                # This is critical because the shell was started with start_new_session=True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except OSError:
                    # Fallback to killing just the process if killpg fails
                    # (e.g., if process is not actually a group leader)
                    process.kill()
            else:
                process.kill()
        except ProcessLookupError:
            pass

    try:
        halt_task = asyncio.create_task(monitor_halt()) if should_halt else None
        timeout_handle = asyncio.get_running_loop().call_later(
            timeout_seconds, on_timeout
        )

        # Stream stdout and stderr concurrently using wait
        stdout_gen = read_stream(process.stdout, STDOUT_FD, output)
        stderr_gen = read_stream(process.stderr, STDERR_FD, output)

        stdout_task = asyncio.create_task(stdout_gen.__anext__())
        stderr_task = asyncio.create_task(stderr_gen.__anext__())
        pending = {stdout_task, stderr_task}

        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                try:
                    piece = await task
                    yield piece

                    # Schedule next read from the same stream
                    # Don't check process.returncode here - we need to drain all buffered output
                    if task is stdout_task and not process.stdout.at_eof():
                        stdout_task = asyncio.create_task(stdout_gen.__anext__())
                        pending.add(stdout_task)
                    elif task is stderr_task and not process.stderr.at_eof():
                        stderr_task = asyncio.create_task(stderr_gen.__anext__())
                        pending.add(stderr_task)
                except StopAsyncIteration:
                    continue

        exit_code = await process.wait()
        timeout_handle.cancel()

    except asyncio.CancelledError:
        # Kill the entire process group when cancelled
        try:
            if uses_process_group:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except OSError:
                    # Fallback to killing just the process if killpg fails
                    process.kill()
            else:
                process.kill()
        except ProcessLookupError:
            pass
        raise
    finally:
        # Explicitly kill the process if it's still running
        if process and process.returncode is None:
            try:
                if uses_process_group:
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except OSError:
                        # Fallback if not a process group leader
                        process.terminate()
                else:
                    process.terminate()
            except ProcessLookupError:
                pass

        tasks_to_cancel: list[asyncio.Task[Any]] = [stdout_task, stderr_task]
        if halt_task:
            tasks_to_cancel.append(halt_task)

        await asyncio.gather(*tasks_to_cancel, return_exceptions=True)

    formatted_output = "".join([chunk for (_, chunk) in output]).strip() + "\n\n"

    yield ShellExecutionResult(
        output=formatted_output,
        cancelled_for_timeout=timed_out,
        exit_code=None if timed_out else exit_code,
        halted=halted,
    )
