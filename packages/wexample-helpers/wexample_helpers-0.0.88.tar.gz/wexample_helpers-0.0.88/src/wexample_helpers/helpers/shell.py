from __future__ import annotations

import asyncio
import shlex
import shutil
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from wexample_helpers.const.types import PathOrString

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

    from wexample_helpers.classes.shell_result import ShellResult
    from wexample_helpers.const.types import PathOrString


def shell_run(
    cmd: str | Sequence[str],
    *,
    cwd: PathOrString | None = None,
    env: Mapping[str, str] | None = None,
    check: bool = True,
    capture: bool = True,
    text: bool = True,
    encoding: str = "utf-8",
    errors: str = "replace",
    timeout: float | None = None,
    shell: bool = False,
    inherit_stdio: bool = False,
    sudo_user: str | None = None,
    elevate: bool = False,
) -> ShellResult:
    """Run a command synchronously with a modern, explicit API.

    Parameters:
    - cmd: Command as str or list[str]. If shell=False (default), str will be shlex-split.
    - cwd/env: Working directory and environment overrides.
    - check: Raise CalledProcessError on non-zero exit (default True).
    - capture: Capture stdout/stderr and return them in result (default True).
    - text/encoding/errors: Text decoding options when capturing output.
    - timeout: Seconds before timing out.
    - shell: Execute through the shell (be explicit; default False).
    - inherit_stdio: If True, inherit parent's stdio (overrides capture).
    - sudo_user/elevate: Optional sudo prefixing; never enabled by default.
    """
    from pathlib import Path

    from wexample_helpers.classes.shell_result import ShellResult

    used_cmd: str | list[str]

    if shell:
        # When using the shell, keep string as-is; if list is provided, join safely.
        if not isinstance(cmd, str):
            used_cmd = shlex.join(cmd)
        else:
            used_cmd = cmd
    else:
        used_cmd = shell_split_cmd(cmd)

    used_cmd = _shell_apply_sudo(
        used_cmd, sudo_user=sudo_user, elevate=elevate, shell=shell
    )

    popen_kwargs: dict[str, Any] = {
        "cwd": cwd,
        "env": env,
        "shell": shell,
    }

    if inherit_stdio:
        # Inherit parent's stdio; no capture.
        stdout = None
        stderr = None
    else:
        if capture:
            stdout = subprocess.PIPE
            stderr = subprocess.PIPE
        else:
            stdout = None
            stderr = None

    start = time.monotonic()
    try:
        completed = subprocess.run(
            used_cmd,  # type: ignore[arg-type]
            stdout=stdout,
            stderr=stderr,
            text=text if capture else False,
            encoding=encoding if (capture and text) else None,
            errors=errors if (capture and text) else None,
            timeout=timeout,
            check=check,
            **popen_kwargs,
        )
        end = time.monotonic()
        return ShellResult(
            args=used_cmd,
            returncode=completed.returncode,
            stdout=completed.stdout if capture else None,
            stderr=completed.stderr if capture else None,
            cwd=Path(cwd) if cwd else None,
            duration=end - start,
            start_time=start,
            end_time=end,
        )
    except subprocess.CalledProcessError as e:
        end = time.monotonic()
        # Re-raise to keep default semantics when check=True
        e.stdout = getattr(e, "stdout", None)
        e.stderr = getattr(e, "stderr", None)
        # Attach timing for debugging/observability
        e.duration = end - start  # type: ignore[attr-defined]
        raise


async def shell_run_async(
    cmd: str | Sequence[str],
    *,
    cwd: str | None = None,
    env: Mapping[str, str] | None = None,
    check: bool = True,
    capture: bool = True,
    text: bool = True,
    encoding: str = "utf-8",
    errors: str = "replace",
    timeout: float | None = None,
    shell: bool = False,
    inherit_stdio: bool = False,
    sudo_user: str | None = None,
    elevate: bool = False,
) -> ShellResult:
    """Run a command asynchronously using asyncio and return a ShellResult.

    If check=True and the return code is non-zero, raises CalledProcessError.
    """
    from pathlib import Path

    from wexample_helpers.classes.shell_result import ShellResult

    used_cmd: str | list[str]

    if shell:
        if not isinstance(cmd, str):
            used_cmd = shlex.join(cmd)
        else:
            used_cmd = cmd
    else:
        used_cmd = shell_split_cmd(cmd)

    used_cmd = _shell_apply_sudo(
        used_cmd, sudo_user=sudo_user, elevate=elevate, shell=shell
    )

    if inherit_stdio:
        stdout_opt = None
        stderr_opt = None
    else:
        stdout_opt = asyncio.subprocess.PIPE if capture else None
        stderr_opt = asyncio.subprocess.PIPE if capture else None

    start = time.monotonic()

    if shell:
        proc = await asyncio.create_subprocess_shell(
            used_cmd if isinstance(used_cmd, str) else " ".join(used_cmd),
            stdout=stdout_opt,
            stderr=stderr_opt,
            cwd=cwd,
            env=dict(env) if env is not None else None,
        )
    else:
        assert isinstance(used_cmd, list)
        proc = await asyncio.create_subprocess_exec(
            *used_cmd,
            stdout=stdout_opt,
            stderr=stderr_opt,
            cwd=cwd,
            env=dict(env) if env is not None else None,
        )

    try:
        if timeout is not None:
            await asyncio.wait_for(proc.wait(), timeout)
            rc = proc.returncode
            out: bytes | None = None
            err: bytes | None = None
            if capture:
                out, err = await proc.communicate()
        else:
            out, err = await proc.communicate() if capture else (None, None)
            rc = proc.returncode
    except TimeoutError:
        proc.kill()
        await proc.wait()
        raise

    end = time.monotonic()

    if capture and text:
        stdout_text = out.decode(encoding, errors) if out is not None else None
        stderr_text = err.decode(encoding, errors) if err is not None else None
    else:
        stdout_text = None
        stderr_text = None

    if check and rc != 0:
        exc = subprocess.CalledProcessError(
            rc, used_cmd, stdout=stdout_text, stderr=stderr_text
        )
        raise exc

    return ShellResult(
        args=used_cmd,
        returncode=rc,
        stdout=stdout_text,
        stderr=stderr_text,
        cwd=Path(cwd),
        duration=end - start,
        start_time=start,
        end_time=end,
    )


def shell_split_cmd(cmd: str | Sequence[str]) -> list[str]:
    """Split a command if provided as a string using shlex; pass lists through."""

    if isinstance(cmd, str):
        return shlex.split(cmd)
    return list(cmd)


async def shell_stream_async(
    cmd: str | Sequence[str],
    *,
    cwd: str | None = None,
    env: Mapping[str, str] | None = None,
    on_stdout: Callable[[str], Any] | None = None,
    on_stderr: Callable[[str], Any] | None = None,
    text: bool = True,
    encoding: str = "utf-8",
    errors: str = "replace",
    shell: bool = False,
    sudo_user: str | None = None,
    elevate: bool = False,
    check: bool = True,
) -> int:
    """Run a command asynchronously and stream stdout/stderr line-by-line.

    - If callbacks are None, default to writing to sys.stdout/sys.stderr.
    - Returns the process return code (and raises if check=True and rc!=0).
    """
    used_cmd: str | list[str]

    if shell:
        if not isinstance(cmd, str):
            used_cmd = shlex.join(cmd)
        else:
            used_cmd = cmd
    else:
        used_cmd = shell_split_cmd(cmd)

    used_cmd = _shell_apply_sudo(
        used_cmd, sudo_user=sudo_user, elevate=elevate, shell=shell
    )

    if shell:
        proc = await asyncio.create_subprocess_shell(
            used_cmd if isinstance(used_cmd, str) else " ".join(used_cmd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=dict(env) if env is not None else None,
        )
    else:
        assert isinstance(used_cmd, list)
        proc = await asyncio.create_subprocess_exec(
            *used_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=dict(env) if env is not None else None,
        )

    async def _pump(
        stream: asyncio.StreamReader, writer: Callable[[str], Any], name: str
    ) -> None:
        while True:
            line = await stream.readline()
            if not line:
                break
            if text:
                s = line.decode(encoding, errors)
            else:
                # Represent raw bytes in a safe way if text=False
                s = line.decode(encoding, errors)
            writer(s)

    def _stdout_writer(s: str) -> None:
        if on_stdout is not None:
            on_stdout(s)
        else:
            sys.stdout.write(s)
            sys.stdout.flush()

    def _stderr_writer(s: str) -> None:
        if on_stderr is not None:
            on_stderr(s)
        else:
            sys.stderr.write(s)
            sys.stderr.flush()

    tasks = []
    if proc.stdout is not None:
        tasks.append(asyncio.create_task(_pump(proc.stdout, _stdout_writer, "stdout")))
    if proc.stderr is not None:
        tasks.append(asyncio.create_task(_pump(proc.stderr, _stderr_writer, "stderr")))

    rc = await proc.wait()
    if tasks:
        await asyncio.gather(*tasks)

    if check and rc != 0:
        raise subprocess.CalledProcessError(rc, used_cmd)
    return rc


def shell_which(cmd: str) -> str | None:
    """Return full path to executable or None if not found (shutil.which wrapper)."""
    return shutil.which(cmd)


def _shell_apply_sudo(
    cmd: str | Sequence[str], *, sudo_user: str | None, elevate: bool, shell: bool
) -> str | list[str]:
    """Prefix the command with sudo options when requested.

    - If shell=True and sudo is requested, we build a string prefix.
    - If shell=False, we build a list prefix.
    """

    if not sudo_user and not elevate:
        return cmd if isinstance(cmd, str) or shell else list(cmd)  # type: ignore[arg-type]

    if shell:
        base = "sudo"
        if sudo_user:
            base += f" -u {shlex.quote(sudo_user)} --"
        elif elevate:
            base += " --"
        if isinstance(cmd, str):
            return f"{base} {cmd}"
        else:
            return f"{base} {shlex.join(cmd)}"
    else:
        prefix: list[str] = ["sudo"]
        if sudo_user:
            prefix += ["-u", sudo_user, "--"]
        elif elevate:
            prefix += ["--"]
        return prefix + (shell_split_cmd(cmd) if isinstance(cmd, str) else list(cmd))
