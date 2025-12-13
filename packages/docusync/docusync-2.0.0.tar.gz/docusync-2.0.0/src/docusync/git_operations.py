"""Git operations for DocuSync."""

import subprocess
from pathlib import Path

from docusync.constants import GIT_COMMAND_TIMEOUT
from docusync.exceptions import GitError
from docusync.logger import USER_LOG


class GitManager:
    """Handles all Git operations."""

    def clone_repository(
        self,
        clone_url: str,
        destination: Path,
        depth: int = 1,
    ) -> None:
        """Clone a Git repository.

        :param clone_url: Repository URL to clone
        :param destination: Destination path
        :param depth: Clone depth (default: 1 for shallow clone)
        :raises GitError: If cloning fails
        """
        USER_LOG.progress_message("Cloning", clone_url)

        cmd = [
            "git",
            "clone",
            "--depth",
            str(depth),
            clone_url,
            str(destination),
        ]

        returncode, stdout, stderr = self._run_command(cmd)

        if returncode != 0:
            raise GitError(f"Failed to clone {clone_url}: {stderr}")

        USER_LOG.debug(f"Clone output: {stdout}")
        USER_LOG.success(f"Cloned successfully: {clone_url}")

    def _run_command(
        self,
        cmd: list[str],
        cwd: Path | None = None,
    ) -> tuple[int, str, str]:
        USER_LOG.command_output(" ".join(cmd))

        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=GIT_COMMAND_TIMEOUT,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as e:
            raise GitError(f"Git command timed out: {' '.join(cmd)}") from e
        except Exception as e:
            raise GitError(f"Failed to run git command: {e}") from e
