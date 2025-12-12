# src/tests/conftest.py
import pytest
from pathlib import Path
import shutil


@pytest.fixture
def file_tree(tmp_path: Path):
    """
    Creates a standard file and directory structure for testing.

    Structure:
    tmp_path/
    ├── empty_dir/
    ├── sub_dir/
    │   ├── nested_image.png
    │   ├── nested_doc.pdf
    │   └── deep_dir/
    │       └── deep_archive.zip
    ├── ignore_this_dir/
    │   └── secret.txt
    ├── main_image.jpg
    ├── main_doc.txt
    ├── main_archive.rar
    ├── script.py
    └── data_report_2023.csv
    """
    # Create top-level files
    (tmp_path / "main_image.jpg").touch()
    (tmp_path / "main_doc.txt").touch()
    (tmp_path / "main_archive.rar").touch()
    (tmp_path / "script.py").touch()
    (tmp_path / "data_report_2023.csv").touch()

    # Create directories
    (tmp_path / "empty_dir").mkdir()
    sub_dir = tmp_path / "sub_dir"
    sub_dir.mkdir()
    deep_dir = sub_dir / "deep_dir"
    deep_dir.mkdir()
    ignore_dir = tmp_path / "ignore_this_dir"
    ignore_dir.mkdir()

    # Create nested files
    (sub_dir / "nested_image.png").touch()
    (sub_dir / "nested_doc.pdf").touch()
    (deep_dir / "deep_archive.zip").touch()
    (ignore_dir / "secret.txt").touch()

    yield tmp_path
    shutil.rmtree(tmp_path)
