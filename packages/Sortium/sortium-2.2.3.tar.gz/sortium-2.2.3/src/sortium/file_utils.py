import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Set, Generator, Sequence, List, Dict

from .config import DEFAULT_IGNORE_ENTRIES


def _build_ignore_set(user_ignore: Sequence[str] | None) -> Set[str]:
    """Combine built-in ignore entries with user supplied ones."""
    return DEFAULT_IGNORE_ENTRIES.union(user_ignore or [])


def _generate_unique_path(dest_path: Path) -> Path:
    """Creates a unique path to avoid overwriting existing files.

    If a file or directory already exists at ``dest_path``, this function
    appends a counter (e.g., " (1)", " (2)") to the file stem until a
    unique path is found.

    Args:
        dest_path: The desired destination path.

    Returns:
        A unique, non-existent path.
    """

    if not dest_path.exists():
        return dest_path

    parent, stem, suffix = dest_path.parent, dest_path.stem, dest_path.suffix
    counter = 1
    while True:
        new_path = parent / f"{stem} ({counter}){suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def _move_file_safely(source_path_str: str, dest_folder_str: str) -> str:
    """Moves a single file while handling destination name collisions."""

    try:
        source_path = Path(source_path_str)
        dest_folder = Path(dest_folder_str)
        dest_folder.mkdir(parents=True, exist_ok=True)
        final_dest_path = _generate_unique_path(dest_folder / source_path.name)
        shutil.move(str(source_path), str(final_dest_path))
        return ""
    except Exception as exc:  # pragma: no cover - surface error for caller
        return f"Error moving file '{source_path_str}': {exc}"


def _move_file_to_path(source_path_str: str, dest_path_str: str) -> str:
    """Moves a file to an explicit destination path without renaming."""

    try:
        source_path = Path(source_path_str)
        dest_path = Path(dest_path_str)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(dest_path))
        return ""
    except Exception as exc:  # pragma: no cover - error string used for diagnostics
        return f"Error moving file '{source_path_str}' -> '{dest_path_str}': {exc}"


class FileUtils:
    """Provides memory-efficient utilities for file and directory manipulation."""

    def get_file_modified_date(self, file_path: str) -> datetime:
        """Returns the last modified datetime of a file.

        Args:
            file_path: Full path to the file.

        Returns:
            A datetime object for the last modification time.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        return datetime.fromtimestamp(path.stat().st_mtime)

    def iter_shallow_files(
        self, folder_path: str, ignore_dir: Sequence[str] | None = None
    ) -> Generator[Path, None, None]:
        """Yields files in the top level of a directory.

        This is a non-recursive generator.

        Args:
            folder_path: Path to the folder to iterate.
            ignore_dir: Additional names to ignore alongside the
                built-in defaults (``DEFAULT_IGNORE_ENTRIES``).

        Yields:
            A generator of ``Path`` objects for each file.
        """
        source_root = Path(folder_path)
        ignore_set = _build_ignore_set(ignore_dir)
        try:
            for item in source_root.iterdir():
                if item.name in ignore_set:
                    continue
                if item.is_file():
                    yield item
        except FileNotFoundError:
            print(f"Directory not found: {folder_path}")
        except PermissionError:
            print(f"Permission denied for directory: {folder_path}")

    def iter_all_files_recursive(
        self, folder_path: str, ignore_dir: Sequence[str] | None = None
    ) -> Generator[Path, None, None]:
        """Recursively yields all files in a directory and its subdirectories.

        This is a memory-efficient generator that does not load the entire
        file list into memory.

        Args:
            folder_path: Path to the root directory to scan.
            ignore_dir: Additional directory names to ignore alongside the
                built-in defaults (``DEFAULT_IGNORE_ENTRIES``).

        Yields:
            A generator of ``Path`` objects for each file found.
        """
        source_root = Path(folder_path)
        if not source_root.is_dir():
            return

        ignore_set = _build_ignore_set(ignore_dir)

        try:
            for item in source_root.iterdir():
                if item.name in ignore_set:
                    continue
                if item.is_dir():
                    yield from self.iter_all_files_recursive(str(item), ignore_dir)
                elif item.is_file():
                    yield item
        except PermissionError:
            print(f"Permission denied for directory: {folder_path}")

    def flatten_dir(
        self,
        folder_path: str,
        dest_folder_path: str,
        ignore_dir: Sequence[str] | None = None,
    ) -> None:
        """Moves all files from a directory tree into a single destination folder.

        This method recursively finds all files in ``folder_path`` and moves
        them to ``dest_folder_path``. It does not preserve the original
        directory structure. It does not delete the original empty folders.

        .. note::
            This operation runs sequentially and does not remove the
            original (now empty) subdirectories.

        Args:
            folder_path: Path to the root folder to flatten.
            dest_folder_path: Path to the single folder where all files will be moved.
            ignore_dir: Additional directory names to ignore alongside the
                built-in defaults (``DEFAULT_IGNORE_ENTRIES``).

        Raises:
            FileNotFoundError: If ``folder_path`` does not exist.
        """
        source_root = Path(folder_path)
        dest_root = Path(dest_folder_path)
        if not source_root.exists():
            raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

        dest_root.mkdir(parents=True, exist_ok=True)

        combined_ignore = tuple(_build_ignore_set(ignore_dir))

        print("Starting directory flattening...")
        for file_path in self.iter_all_files_recursive(
            str(source_root), combined_ignore
        ):
            error_msg = _move_file_safely(str(file_path), str(dest_root))
            if error_msg:
                print(error_msg)
        print("Flattening complete.")

    def find_unique_extensions(
        self, source_path: str, ignore_dir: List[str] | None = None
    ) -> Set[str]:
        """Recursively finds all unique file extensions in a directory.

        This method is memory-efficient, scanning the directory tree without
        loading all paths into memory at once.

        Args:
            source_path: Path to the root directory to scan.
            ignore_dir: Additional directory names to ignore alongside the
                built-in defaults (``DEFAULT_IGNORE_ENTRIES``).

        Returns:
            A set of unique file extensions (e.g., {".txt", ".jpg"}).

        Raises:
            FileNotFoundError: If ``source_path`` does not exist.
        """
        source_root = Path(source_path)
        if not source_root.exists():
            raise FileNotFoundError(f"The path '{source_root}' does not exist.")

        extensions: Set[str] = set()
        file_generator = self.iter_all_files_recursive(
            str(source_root), tuple(_build_ignore_set(ignore_dir))
        )

        for file_path in file_generator:
            if file_path.suffix:
                extensions.add(file_path.suffix.lower())

        return extensions

    def export_directory_structure(
        self,
        folder_path: str,
        output_file: str,
        ignore_dir: Sequence[str] | None = None,
    ) -> Path:
        """Writes the directory tree rooted at ``folder_path`` to a JSON file.

        Args:
            folder_path: Directory whose structure should be traced.
            output_file: Destination JSON file path.
            ignore_dir: Optional iterable of additional directory or file names
                to skip alongside ``DEFAULT_IGNORE_ENTRIES``.

        Returns:
            Path to the generated JSON file.

        Raises:
            FileNotFoundError: If ``folder_path`` does not exist.
            NotADirectoryError: If ``folder_path`` is not a directory.
        """

        source_root = Path(folder_path)
        if not source_root.exists():
            raise FileNotFoundError(
                f"The path '{folder_path}' does not exist and cannot be exported."
            )
        if not source_root.is_dir():
            raise NotADirectoryError(
                f"The path '{folder_path}' is not a directory and cannot be exported."
            )

        ignore_set = _build_ignore_set(ignore_dir)

        def build_node(current_path: Path) -> dict:
            if current_path.is_file():
                try:
                    size = current_path.stat().st_size
                except (PermissionError, OSError):
                    size = None
                return {
                    "name": current_path.name,
                    "path": str(current_path),
                    "type": "file",
                    "size": size,
                }

            children = []
            try:
                for child in sorted(
                    current_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())
                ):
                    if child.name in ignore_set:
                        continue
                    child_snapshot = build_node(child)
                    if child_snapshot is not None:
                        children.append(child_snapshot)
            except PermissionError:
                # Surface the permission error at this directory level.
                return {
                    "name": current_path.name,
                    "path": str(current_path),
                    "type": "directory",
                    "children": [],
                    "error": "permission-denied",
                }

            return {
                "name": current_path.name,
                "path": str(current_path),
                "type": "directory",
                "children": children,
            }

        snapshot = build_node(source_root)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as json_file:
            json.dump(snapshot, json_file, indent=2)

        return output_path

    def plan_destination_path(self, source_path: str, dest_folder_path: str) -> Path:
        """Predicts the collision-safe destination path for a file move.

        Args:
            source_path: Current location of the file.
            dest_folder_path: Folder where the file is planned to be moved.

        Returns:
            Path of the file at the destination, including any rename that
            would be required to avoid collisions.
        """

        source = Path(source_path)
        dest_folder = Path(dest_folder_path)
        return _generate_unique_path(dest_folder / source.name)

    def apply_move_plan(
        self,
        plan_file: str,
        reverse: bool = False,
        dry_run: bool = False,
    ) -> Dict[str, int | List[str]]:
        """Applies or reverses a JSON move plan produced by Sorter methods.

        Args:
            plan_file: Path to the JSON plan file to execute.
            reverse: If ``True``, moves files back to their ``source_path``.
            dry_run: If ``True``, validates the plan without moving files.

        Returns:
            A summary dictionary containing ``entries``, ``moved`` and
            ``errors`` keys.

        Raises:
            FileNotFoundError: If ``plan_file`` does not exist.
        """

        plan_path = Path(plan_file)
        if not plan_path.is_file():
            raise FileNotFoundError(f"Plan file '{plan_file}' does not exist.")

        with plan_path.open("r", encoding="utf-8") as plan_stream:
            plan_payload = json.load(plan_stream)

        entries = plan_payload.get("entries", [])
        if dry_run:
            return {"entries": len(entries), "moved": 0, "errors": []}

        errors: List[str] = []
        moved = 0

        source_key = "destination_path" if reverse else "source_path"
        dest_key = "source_path" if reverse else "destination_path"

        for idx, entry in enumerate(entries):
            if entry.get("skip"):
                continue

            source_val = entry.get(source_key)
            dest_val = entry.get(dest_key)
            if not source_val or not dest_val:
                errors.append(
                    f"Entry #{idx} is missing required keys '{source_key}' or '{dest_key}'."
                )
                continue

            source = Path(source_val)
            dest = Path(dest_val)
            if not source.exists():
                errors.append(f"Source path does not exist: {source}")
                continue
            if dest.exists():
                errors.append(
                    f"Destination already exists (plan stale?): {dest}"
                )
                continue

            error_msg = _move_file_to_path(str(source), str(dest))
            if error_msg:
                errors.append(error_msg)
            else:
                moved += 1

        return {"entries": len(entries), "moved": moved, "errors": errors}
