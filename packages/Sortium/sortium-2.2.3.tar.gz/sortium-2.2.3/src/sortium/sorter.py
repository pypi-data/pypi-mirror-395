import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

from .config import DEFAULT_FILE_TYPES
from .file_utils import FileUtils


class Sorter:
    """Organizes files into directories based on various criteria.

    Each public method emits a JSON move plan describing every file's source
    and destination so you can review, edit, or auto-apply the workflow. The
    class stays memory-efficient while handling large trees by relying on
    generators and incremental planning.

    Attributes:
        file_types_dict (Dict[str, List[str]]): A mapping of file category
            names to lists of associated file extensions.
        file_utils (FileUtils): An instance of a file utility class.
    """

    def __init__(
        self,
        file_types_dict: Dict[str, List[str]] = None,
        file_utils: FileUtils = None,
    ):
        """Initializes the Sorter instance.

        Args:
            file_types_dict (Dict[str, List[str]], optional): A dictionary
                mapping category names to file extensions. Defaults to
                ``DEFAULT_FILE_TYPES``.
            file_utils (FileUtils, optional): An instance of FileUtils.
                Defaults to a new ``FileUtils()`` instance.
        """
        self.file_types_dict = file_types_dict or DEFAULT_FILE_TYPES
        self.file_utils = file_utils or FileUtils()
        self.extension_to_category = {
            ext.lower(): category
            for category, extensions in self.file_types_dict.items()
            for ext in extensions
        }

    def _get_category(self, extension: str) -> str:
        """Determines the category for a file extension.

        Args:
            extension: The file extension (e.g., ".pdf").

        Returns:
            The corresponding category name (e.g., "Documents") or "Others".
        """
        return self.extension_to_category.get(extension.lower(), "Others")

    def _resolve_plan_path(
        self, base_folder: Path, strategy: str, plan_output: str | None
    ) -> Path:
        """Determines where a plan JSON should be written.

        Args:
            base_folder: Folder whose name seeds the default plan location.
            strategy: The sorting strategy name (e.g., "type").
            plan_output: Optional explicit path supplied by the caller.

        Returns:
            Absolute path where the JSON plan will be saved.
        """

        if plan_output:
            return Path(plan_output)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return base_folder / f"sortium_plan_{strategy}_{timestamp}.json"

    def _write_plan(
        self,
        strategy: str,
        source_root: Path,
        destination_root: Path,
        entries: List[Dict[str, Any]],
        plan_output: str | None,
        extra_metadata: Dict[str, Any] | None = None,
    ) -> Path:
        """Persists a move plan to disk and returns the resulting path.

        Args:
            strategy: Sorting strategy identifier (type/date/regex/extension).
            source_root: Root directory scanned when generating the plan.
            destination_root: Base directory files will ultimately move into.
            entries: List of per-file plan entries.
            plan_output: Optional custom path for the output JSON file.
            extra_metadata: Optional dictionary merged into the plan payload.

        Returns:
            Path to the serialized JSON plan on disk.
        """

        plan_payload: Dict[str, Any] = {
            "plan_id": str(uuid4()),
            "version": 1,
            "strategy": strategy,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_root": str(source_root),
            "destination_root": str(destination_root),
            "entry_count": len(entries),
            "entries": entries,
        }
        if extra_metadata:
            plan_payload["metadata"] = extra_metadata

        plan_path = self._resolve_plan_path(source_root, strategy, plan_output)
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        with plan_path.open("w", encoding="utf-8") as plan_file:
            json.dump(plan_payload, plan_file, indent=2)

        print(
            f"Sort plan for strategy '{strategy}' written to '{plan_path}'."
        )
        return plan_path

    def sort_by_type(
        self,
        folder_path: str,
        dest_folder_path: str | None = None,
        ignore_dir: List[str] | None = None,
        plan_output: str | None = None,
        auto_apply: bool = False,
        recursive: bool = False,
    ) -> Path:
        """Generates a plan to sort files into subdirectories by file type.

        Files in the top level of ``folder_path`` are mapped into subdirectories
        (e.g., "Images", "Documents") inside ``dest_folder_path``. Enable
        ``recursive`` to scan the entire tree. The plan is written to JSON so it
        can be inspected or edited before execution.

        .. note:: This method is memory-efficient and suitable for sorting
                  directories with a very large number of files.

        Args:
            folder_path: Path to the directory containing unsorted files.
            dest_folder_path: Base directory for the sorted category folders.
                Falls back to ``folder_path`` when ``None``.
            ignore_dir: Optional directory names to skip when scanning.
            plan_output: Optional JSON path override for the emitted plan.
            auto_apply: If ``True``, immediately executes the generated plan.
            recursive: When ``True``, recursively scans nested folders.

        Returns:
            Path to the JSON plan file.

        Raises:
            FileNotFoundError: If ``folder_path`` does not exist.
        """
        source_folder = Path(folder_path)
        if not source_folder.exists():
            raise FileNotFoundError(f"The path '{source_folder}' does not exist.")
        dest_base_folder = Path(dest_folder_path) if dest_folder_path else source_folder

        entries: List[Dict[str, Any]] = []
        file_iterator = (
            self.file_utils.iter_all_files_recursive(str(source_folder), ignore_dir)
            if recursive
            else self.file_utils.iter_shallow_files(str(source_folder), ignore_dir)
        )

        for item in file_iterator:
            category = self._get_category(item.suffix)
            dest_folder = dest_base_folder / category
            planned_path = self.file_utils.plan_destination_path(
                str(item), str(dest_folder)
            )
            entries.append(
                {
                    "source_path": str(item),
                    "destination_path": str(planned_path),
                    "category": category,
                    "extension": item.suffix.lower(),
                }
            )

        plan_path = self._write_plan(
            strategy="type",
            source_root=source_folder,
            destination_root=dest_base_folder,
            entries=entries,
            plan_output=plan_output,
            extra_metadata={
                "ignored": list(ignore_dir or []),
                "file_types": self.file_types_dict,
                "recursive": recursive,
            },
        )

        if auto_apply:
            self.file_utils.apply_move_plan(str(plan_path))

        return plan_path

    def sort_by_date(
        self,
        folder_path: str,
        folder_types: List[str],
        dest_folder_path: str | None = None,
        plan_output: str | None = None,
        auto_apply: bool = False,
        recursive: bool = False,
    ) -> Path:
        """Generates a plan to sort files within categories by modification date.

        Files are moved into date-stamped subfolders (e.g., "01-Jan-2023"). Set
        ``recursive`` to pull in files from nested directories within each
        category.

        Args:
            folder_path: Root directory containing the category folders to process.
            folder_types: List of category folder names (e.g., ['Images']).
            dest_folder_path: Base directory for the sorted folders. Defaults
                to ``folder_path`` when ``None``.
            plan_output: Optional JSON path override for the emitted plan.
            auto_apply: If ``True``, immediately executes the generated plan.
            recursive: When ``True``, scans inside nested directories under
                each category.

        Returns:
            Path to the JSON plan file.

        Raises:
            FileNotFoundError: If ``folder_path`` does not exist.
        """
        source_root = Path(folder_path)
        if not source_root.exists():
            raise FileNotFoundError(f"The path '{source_root}' does not exist.")
        dest_root = Path(dest_folder_path) if dest_folder_path else source_root

        entries: List[Dict[str, Any]] = []
        for folder_type in folder_types:
            category_folder = source_root / folder_type
            if not category_folder.is_dir():
                print(f"Category folder '{category_folder}' not found, skipping.")
                continue

            if recursive:
                file_iter = self.file_utils.iter_all_files_recursive(
                    str(category_folder)
                )
            else:
                file_iter = category_folder.iterdir()

            for file_path in file_iter:
                if not file_path.is_file():
                    continue

                try:
                    modified = self.file_utils.get_file_modified_date(str(file_path))
                except Exception as exc:
                    print(f"Could not evaluate file '{file_path.name}': {exc}")
                    continue

                date_str = modified.strftime("%d-%b-%Y")
                final_dest_folder = dest_root / folder_type / date_str
                planned_path = self.file_utils.plan_destination_path(
                    str(file_path), str(final_dest_folder)
                )
                entries.append(
                    {
                        "source_path": str(file_path),
                        "destination_path": str(planned_path),
                        "category": folder_type,
                        "date_folder": date_str,
                        "modified_at": modified.isoformat(),
                    }
                )

        plan_path = self._write_plan(
            strategy="date",
            source_root=source_root,
            destination_root=dest_root,
            entries=entries,
            plan_output=plan_output,
            extra_metadata={
                "folder_types": folder_types,
                "recursive": recursive,
            },
        )

        if auto_apply:
            self.file_utils.apply_move_plan(str(plan_path))

        return plan_path

    def sort_by_regex(
        self,
        folder_path: str,
        regex: Dict[str, str],
        dest_folder_path: str,
        plan_output: str | None = None,
        auto_apply: bool = False,
        recursive: bool = True,
    ) -> Path:
        """Generates a plan to sort files recursively based on regex patterns.

        Scans ``folder_path`` (optionally including subdirectories) for files
        whose names match the provided regex patterns, then moves them to
        categorized folders within ``dest_folder_path``.

        Args:
            folder_path: Path to the directory to scan recursively.
            regex: Dictionary mapping category names to regex patterns.
            dest_folder_path: Base directory where sorted files will be moved.
            plan_output: Optional JSON path override for the emitted plan.
            auto_apply: If ``True``, immediately executes the generated plan.
            recursive: When ``True`` (default), recursively scans the folder.

        Returns:
            Path to the JSON plan file.

        Raises:
            FileNotFoundError: If ``folder_path`` does not exist.
            RuntimeError: If a critical error occurs while preparing the plan.
        """
        source_path = Path(folder_path)
        if not source_path.exists():
            raise FileNotFoundError(f"The path '{source_path}' does not exist.")
        dest_base_path = Path(dest_folder_path)

        entries: List[Dict[str, Any]] = []
        file_generator = (
            self.file_utils.iter_all_files_recursive(str(source_path))
            if recursive
            else self.file_utils.iter_shallow_files(str(source_path))
        )
        for file_path in file_generator:
            for category, pattern in regex.items():
                if re.match(pattern, file_path.name):
                    dest_folder = dest_base_path / category
                    planned_path = self.file_utils.plan_destination_path(
                        str(file_path), str(dest_folder)
                    )
                    entries.append(
                        {
                            "source_path": str(file_path),
                            "destination_path": str(planned_path),
                            "category": category,
                            "pattern": pattern,
                        }
                    )
                    break

        plan_path = self._write_plan(
            strategy="regex",
            source_root=source_path,
            destination_root=dest_base_path,
            entries=entries,
            plan_output=plan_output,
            extra_metadata={"regex": regex, "recursive": recursive},
        )

        if auto_apply:
            self.file_utils.apply_move_plan(str(plan_path))

        return plan_path

    def sort_by_extension(
        self,
        folder_path: str,
        dest_folder_path: str | None = None,
        ignore_dir: List[str] | None = None,
        plan_output: str | None = None,
        auto_apply: bool = False,
        recursive: bool = True,
    ) -> Path:
        """Generates a plan to sort files by extension into subdirectories.

        Args:
            folder_path: Path to the directory containing unsorted files.
            dest_folder_path: Base directory for the sorted category folders.
                Falls back to ``folder_path`` when ``None``.
            ignore_dir: Optional directory names to skip when scanning.
            plan_output: Optional JSON path override for the emitted plan.
            auto_apply: If ``True``, immediately executes the generated plan.
            recursive: When ``True`` (default), recursively scans the tree.

        Returns:
            Path to the JSON plan file.

        Raises:
            FileNotFoundError: If ``folder_path`` does not exist.
        """
        source_folder = Path(folder_path)
        if not source_folder.exists():
            raise FileNotFoundError(f"The path '{source_folder}' does not exist.")
        dest_base_folder = Path(dest_folder_path) if dest_folder_path else source_folder

        entries: List[Dict[str, Any]] = []
        file_iterator = (
            self.file_utils.iter_all_files_recursive(str(source_folder), ignore_dir)
            if recursive
            else self.file_utils.iter_shallow_files(str(source_folder), ignore_dir)
        )

        for item in file_iterator:
            extension = item.suffix.lower().lstrip(".")
            dest_folder = dest_base_folder / extension if extension else dest_base_folder
            planned_path = self.file_utils.plan_destination_path(
                str(item), str(dest_folder)
            )
            entries.append(
                {
                    "source_path": str(item),
                    "destination_path": str(planned_path),
                    "extension": extension,
                }
            )

        plan_path = self._write_plan(
            strategy="extension",
            source_root=source_folder,
            destination_root=dest_base_folder,
            entries=entries,
            plan_output=plan_output,
            extra_metadata={
                "ignored": list(ignore_dir or []),
                "recursive": recursive,
            },
        )

        if auto_apply:
            self.file_utils.apply_move_plan(str(plan_path))

        return plan_path
