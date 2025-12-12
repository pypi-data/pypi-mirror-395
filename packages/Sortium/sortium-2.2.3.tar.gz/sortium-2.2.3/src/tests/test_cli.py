"""Integration-style tests for the Sortium CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sortium.cli import main as cli_main


def _run_cli(args: list[str]) -> None:
    """Helper to invoke the CLI entry point in tests."""
    cli_main(args)


def test_cli_plan_generates_recursive_plan(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "nested").mkdir()
    (source / "nested" / "file.txt").write_text("note")
    plan_path = tmp_path / "plan.json"

    _run_cli(
        [
            "plan",
            "type",
            "--source",
            str(source),
            "--plan-output",
            str(plan_path),
            "--recursive",
        ]
    )

    payload = json.loads(plan_path.read_text())
    assert payload["entry_count"] == 1
    assert payload["metadata"]["recursive"] is True
    entry = payload["entries"][0]
    assert entry["source_path"].endswith("file.txt")


def test_cli_apply_and_undo(tmp_path: Path) -> None:
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    source.mkdir()
    (source / "main_doc.txt").write_text("content")
    plan_path = tmp_path / "plan.json"

    _run_cli(
        [
            "plan",
            "type",
            "--source",
            str(source),
            "--dest",
            str(dest),
            "--plan-output",
            str(plan_path),
        ]
    )

    _run_cli(["apply", "--plan", str(plan_path)])
    moved_file = dest / "Documents" / "main_doc.txt"
    assert moved_file.is_file()
    assert not (source / "main_doc.txt").exists()

    _run_cli(["undo", "--plan", str(plan_path)])
    assert (source / "main_doc.txt").is_file()
    assert not moved_file.exists()


def test_cli_tree_exports_snapshot(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    (root / "report.md").write_text("hello")
    tree_output = tmp_path / "tree.json"

    _run_cli(
        [
            "tree",
            "--source",
            str(root),
            "--output",
            str(tree_output),
        ]
    )

    snapshot = json.loads(tree_output.read_text())
    assert snapshot["type"] == "directory"
    child_names = {child["name"] for child in snapshot["children"]}
    assert "report.md" in child_names
