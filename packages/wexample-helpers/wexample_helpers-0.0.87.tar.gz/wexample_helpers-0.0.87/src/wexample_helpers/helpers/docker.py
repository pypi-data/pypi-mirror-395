# docker_helpers.py
from __future__ import annotations

from pathlib import Path

from wexample_helpers.helpers.shell import shell_run


def docker_build_image(image_name: str, dockerfile_path: Path) -> None:
    """Build a Docker image."""
    build_context = dockerfile_path.parent

    shell_run(
        cmd=[
            "docker",
            "build",
            "-t",
            image_name,
            "-f",
            str(dockerfile_path),
            str(build_context),
        ],
        inherit_stdio=True,
    )


def docker_build_name_from_path(
    root_path: str | Path, image_name: str, prefix: str = "wex"
) -> str:
    """
    Generate a deterministic Docker container name based on the root path
    and the Docker image name.

    Args:
        root_path: Absolute path of the application root.
        image_name: Docker image name.
        prefix: Optional prefix for the container name.

    Returns:
        A unique and reproducible container name.
    """
    import hashlib

    root_path = str(Path(root_path).resolve())
    path_hash = hashlib.md5(root_path.encode()).hexdigest()[:8]
    return f"{prefix}-{image_name}-{path_hash}"


def docker_container_exists(container_name: str) -> bool:
    """Check if a Docker container exists (running or stopped)."""
    result = shell_run(
        cmd=["docker", "ps", "-a", "-q", "-f", f"name={container_name}"], capture=True
    )
    return bool(result.stdout.strip())


def docker_container_is_running(container_name: str) -> bool:
    """Check if a Docker container is currently running."""
    result = shell_run(
        cmd=["docker", "ps", "-q", "-f", f"name={container_name}"], capture=True
    )
    return bool(result.stdout.strip())


def docker_exec(
    container_name: str, command: list[str], user: str | None = None
) -> str:
    """Execute a command inside a running Docker container.

    Args:
        container_name: Name of the container
        command: Command to execute
        user: Optional user specification (e.g., "1000:1000" or "username")
    """
    cmd = ["docker", "exec"]
    if user:
        cmd += ["--user", user]
    cmd += [container_name] + command
    result = shell_run(cmd=cmd, capture=True)
    return result.stdout


def docker_image_exists(image_name: str) -> bool:
    """Return True if the Docker image already exists."""
    result = shell_run(cmd=["docker", "images", "-q", image_name], capture=True)
    return bool(result.stdout.strip())


def docker_remove_container(container_name: str) -> None:
    """Remove a Docker container."""
    shell_run(cmd=["docker", "rm", container_name], inherit_stdio=True)


def docker_remove_image(image_name: str) -> None:
    """Remove a Docker image."""
    shell_run(cmd=["docker", "rmi", image_name], inherit_stdio=True)


def docker_run_container(
    container_name: str,
    image_name: str,
    volumes: dict[str, str],
    user: str | None = None,
) -> None:
    """Run a new container.

    Args:
        container_name: Name for the container
        image_name: Docker image to use
        volumes: Dictionary of host:container volume mappings
        user: Optional user specification (e.g., "1000:1000" or "username")
    """
    cmd = [
        "docker",
        "run",
        "-d",
        "--name",
        container_name,
    ]

    if user:
        cmd += ["--user", user]

    for host, container in volumes.items():
        cmd += ["-v", f"{host}:{container}"]

    cmd.append(image_name)

    shell_run(cmd, inherit_stdio=True)


def docker_start_container(container_name: str) -> None:
    """Start an existing stopped container."""
    shell_run(cmd=["docker", "start", container_name], inherit_stdio=True)


def docker_stop_container(container_name: str) -> None:
    """Stop a running Docker container."""
    shell_run(cmd=["docker", "stop", container_name], inherit_stdio=True)
