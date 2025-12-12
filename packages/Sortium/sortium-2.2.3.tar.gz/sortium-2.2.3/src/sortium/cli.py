"""Command-line interface for Sortium."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

from .file_utils import FileUtils
from .sorter import Sorter


def _add_plan_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    plan_parser = subparsers.add_parser(
        "plan",
        help="Generate a JSON move plan using one of the available strategies",
    )
    plan_parser.add_argument(
        "strategy",
        choices=["type", "extension", "regex", "date"],
        help="Sorting strategy to use",
    )
    plan_parser.add_argument(
        "--source",
        required=True,
        help="Path to the source folder to analyze",
    )
    plan_parser.add_argument(
        "--dest",
        help="Optional destination folder (defaults to source)",
    )
    plan_parser.add_argument(
        "--plan-output",
        dest="plan_output",
        help="Optional path where the plan JSON should be written",
    )
    plan_parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="Directory or file names to ignore while scanning",
    )
    plan_parser.add_argument(
        "--recursive",
        dest="recursive",
        action="store_true",
        help="Scan subdirectories recursively",
    )
    plan_parser.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Force a shallow scan (files in the root only)",
    )
    plan_parser.set_defaults(recursive=None)
    plan_parser.add_argument(
        "--regex",
        nargs="*",
        help="Regex rules for the regex strategy in CATEGORY=PATTERN form",
    )
    plan_parser.add_argument(
        "--regex-file",
        help="Path to a JSON file containing category-pattern pairs",
    )
    plan_parser.add_argument(
        "--folder-type",
        dest="folder_types",
        action="append",
        help="Category folder to process for the date strategy (repeatable)",
    )
    plan_parser.set_defaults(func=_handle_plan)


def _add_apply_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    apply_parser = subparsers.add_parser(
        "apply",
        help="Execute a previously generated JSON plan",
    )
    apply_parser.add_argument(
        "--plan",
        required=True,
        help="Path to the plan JSON to execute",
    )
    apply_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the plan without moving files",
    )
    apply_parser.set_defaults(reverse=False)
    apply_parser.add_argument(
        "--reverse",
        action="store_true",
        help="Reverse a plan by moving files back to their original locations",
    )
    apply_parser.set_defaults(func=_handle_apply)


def _add_undo_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    undo_parser = subparsers.add_parser(
        "undo",
        help="Shortcut for reversing a plan (equivalent to apply --reverse)",
    )
    undo_parser.add_argument(
        "--plan",
        required=True,
        help="Path to the plan JSON that should be reversed",
    )
    undo_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the rollback plan without moving files",
    )
    undo_parser.set_defaults(func=_handle_undo)


def _add_tree_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    tree_parser = subparsers.add_parser(
        "tree",
        help="Export a snapshot of a directory structure as JSON",
    )
    tree_parser.add_argument(
        "--source",
        required=True,
        help="Root folder to snapshot",
    )
    tree_parser.add_argument(
        "--output",
        help="Destination JSON file (defaults to <source>/sortium_tree.json)",
    )
    tree_parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="Names to ignore while traversing",
    )
    tree_parser.set_defaults(func=_handle_tree)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sortium",
        description="Command-line interface for generating and applying Sortium plans",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_plan_parser(subparsers)
    _add_apply_parser(subparsers)
    _add_undo_parser(subparsers)
    _add_tree_parser(subparsers)
    return parser


def _determine_recursive(strategy: str, requested: bool | None) -> bool:
    if requested is not None:
        return requested
    return strategy in {"extension", "regex"}


def _load_regex_mapping(args: argparse.Namespace) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if args.regex:
        for pair in args.regex:
            if "=" not in pair:
                raise SystemExit("Regex rules must be provided as CATEGORY=PATTERN")
            category, pattern = pair.split("=", 1)
            mapping[category.strip()] = pattern.strip()
    if args.regex_file:
        try:
            data: Any
            with open(args.regex_file, "r", encoding="utf-8") as regex_stream:
                data = json.load(regex_stream)
        except FileNotFoundError as exc:  # pragma: no cover - surfaced to user
            raise SystemExit(f"Regex file not found: {exc}")
        except json.JSONDecodeError as exc:  # pragma: no cover - surfaced to user
            raise SystemExit(f"Regex file must contain valid JSON: {exc}")
        if not isinstance(data, dict):
            raise SystemExit("Regex file must contain an object mapping categories to patterns")
        for key, value in data.items():
            mapping[str(key)] = str(value)
    return mapping


def _handle_plan(args: argparse.Namespace) -> Path:
    sorter = Sorter()
    ignore = args.ignore or []
    recursive = _determine_recursive(args.strategy, args.recursive)

    if args.strategy == "type":
        plan_path = sorter.sort_by_type(
            folder_path=args.source,
            dest_folder_path=args.dest,
            ignore_dir=ignore,
            plan_output=args.plan_output,
            recursive=recursive,
        )
    elif args.strategy == "extension":
        plan_path = sorter.sort_by_extension(
            folder_path=args.source,
            dest_folder_path=args.dest,
            ignore_dir=ignore,
            plan_output=args.plan_output,
            recursive=recursive,
        )
    elif args.strategy == "regex":
        regex_map = _load_regex_mapping(args)
        if not regex_map:
            raise SystemExit("Regex strategy requires --regex or --regex-file")
        destination = args.dest or args.source
        plan_path = sorter.sort_by_regex(
            folder_path=args.source,
            regex=regex_map,
            dest_folder_path=destination,
            plan_output=args.plan_output,
            recursive=recursive,
        )
    elif args.strategy == "date":
        folder_types: Sequence[str] | None = args.folder_types
        if not folder_types:
            raise SystemExit("Date strategy requires at least one --folder-type value")
        plan_path = sorter.sort_by_date(
            folder_path=args.source,
            folder_types=list(folder_types),
            dest_folder_path=args.dest,
            plan_output=args.plan_output,
            recursive=recursive,
        )
    else:  # pragma: no cover - parser restricts choices
        raise SystemExit(f"Unsupported strategy '{args.strategy}'")

    print(f"Plan written to {plan_path}")
    return plan_path


def _handle_apply(args: argparse.Namespace) -> Dict[str, Any]:
    file_utils = FileUtils()
    summary = file_utils.apply_move_plan(
        plan_file=args.plan,
        reverse=args.reverse,
        dry_run=args.dry_run,
    )
    print(json.dumps(summary, indent=2))
    return summary


def _handle_undo(args: argparse.Namespace) -> Dict[str, Any]:
    args_for_apply = argparse.Namespace(
        plan=args.plan,
        dry_run=args.dry_run,
        reverse=True,
    )
    return _handle_apply(args_for_apply)


def _handle_tree(args: argparse.Namespace) -> Path:
    source = Path(args.source)
    output = Path(args.output) if args.output else source / "sortium_tree.json"
    file_utils = FileUtils()
    result = file_utils.export_directory_structure(
        folder_path=str(source),
        output_file=str(output),
        ignore_dir=args.ignore,
    )
    print(f"Structure exported to {result}")
    return result


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
