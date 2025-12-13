"""File system operations for DocuSync."""

import json
import shutil
from pathlib import Path

from docusync.exceptions import FileOperationError
from docusync.logger import USER_LOG


class FileManager:
    """Handles all file system operations."""

    def ensure_directory(self, path: Path) -> None:
        """Ensure a directory exists.

        :param path: Directory path1`
        :raises FileOperationError: If directory creation fails
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            USER_LOG.debug(f"Ensured directory exists: {path}")
        except OSError as e:
            raise FileOperationError(
                f"Failed to create directory {path}: {e}"
            ) from e

    def remove_directory(self, path: Path) -> None:
        """Remove a directory and all its contents.

        :param path: Directory path to remove
        :raises FileOperationError: If removal fails
        """
        if not path.exists():
            return

        try:
            USER_LOG.warning(f"Removing directory: {path}")
            shutil.rmtree(path)
        except OSError as e:
            raise FileOperationError(
                f"Failed to remove directory {path}: {e}"
            ) from e

    def copy_directory(self, source: Path, destination: Path) -> None:
        """Copy a directory from source to destination.

        :param source: Source directory
        :param destination: Destination directory
        :raises FileOperationError: If source doesn't exist or copy fails
        """
        if not source.exists():
            raise FileOperationError(
                f"Source directory does not exist: {source}"
            )

        if not source.is_dir():
            raise FileOperationError(f"Source is not a directory: {source}")

        try:
            # Remove destination if it exists
            if destination.exists():
                USER_LOG.warning(
                    f"Destination exists, removing: {destination}"
                )
                shutil.rmtree(destination)

            USER_LOG.progress_message("Copying", f"{source} → {destination}")
            shutil.copytree(source, destination)
            USER_LOG.debug(f"Successfully copied {source} to {destination}")
        except OSError as e:
            raise FileOperationError(
                f"Failed to copy {source} to {destination}: {e}"
            ) from e

    def create_category_file(
        self,
        directory: Path,
        label: str,
        position: int,
        description: str,
    ) -> None:
        """Create a _category_.json file for Docusaurus.

        :param directory: Directory to create the file in
        :param label: Category label
        :param position: Category position in sidebar
        :param description: Category description
        :raises FileOperationError: If file creation fails
        """
        category_data = {
            "label": label,
            "position": position,
            "link": {
                "type": "generated-index",
                "description": description,
            },
        }

        category_file = directory / "_category_.json"

        try:
            USER_LOG.progress_message(
                "Creating", f"_category_.json in {directory.name}"
            )
            with open(category_file, "w", encoding="utf-8") as f:
                json.dump(category_data, f, indent=2, ensure_ascii=False)
                f.write("\n")  # Add trailing newline
            USER_LOG.debug(f"Created category file: {category_file}")
        except OSError as e:
            raise FileOperationError(
                f"Failed to create category file {category_file}: {e}"
            ) from e
