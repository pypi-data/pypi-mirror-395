# `sortium` Test Suite

This directory contains a complete suite of tests for the `sortium` Python library—a utility for organizing and sorting files with a plan-first workflow.

The test suite ensures correctness, robustness, and graceful handling of errors across the library's core features, including plan generation/apply flows, recursive file scanning, and name collision avoidance.

## 📁 Directory Overview

```
tests/
│
├── conftest.py            # Shared fixtures, including the primary `file_tree` structure.
├── test_sorter.py         # Tests for the core Sorter class and its sorting logic.
└── test_file_utils.py     # Tests for file system utilities (generators, flattening, etc.).
```

---

## What’s Tested

### `test_sorter.py`

Tests the `Sorter` class, which is responsible for the main file organization logic.

- **`sort_by_type()`**

  - Correctly categorizes files into folders like `Images`, `Documents`, etc.
  - Successfully sorts files to a **separate destination directory**.
  - Gracefully handles **file name collisions** by creating unique names (e.g., `file (1).txt`).
  - Raises `FileNotFoundError` for invalid source paths.

- **`sort_by_date()`**

  - Sorts files within existing category folders into date-stamped subfolders (e.g., `01-Jan-2023`).
  - Verifies correct placement of files within the new date folders.
  - Skips non-existent category folders without error.

- **`sort_by_regex()`**
  - Performs **recursive** scanning to find matching files in nested directories.
  - Categorizes files based on complex regex patterns.
  - Verifies that files from deep subdirectories are correctly moved.

---

### `test_file_utils.py`

Tests the `FileUtils` class and its helper functions, which provide the building blocks for file system operations.

- **File Iterators (`iter_shallow_files` & `iter_all_files_recursive`)**

  - Verifies that the generators yield the correct files.
  - Confirms that `ignore_dir` properly excludes specified directories.
  - Ensures recursive iteration correctly traverses the entire directory tree.

- **`flatten_dir()`**

  - Moves all files from a nested directory structure into a single destination folder.
  - Correctly respects the `ignore_dir` parameter.
  - Raises `FileNotFoundError` for invalid source paths.

- **`find_unique_extensions()`**

  - Accurately detects and returns all unique file extensions from a directory tree.
  - Validates that ignored directories are excluded from the scan.

- **Helper Functions**
  - Tests `get_file_modified_date()` for correctness.
  - Validates the name collision logic in `_generate_unique_path()`.

---

## Primary Test Fixture: `file_tree`

To ensure consistent and isolated tests, a primary fixture named `file_tree` is defined in `conftest.py`. It creates a temporary directory with a standard nested structure for most tests to use.

```
<tmp_path>/
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
```

This structure allows tests to validate shallow scanning, deep recursion, and directory exclusion logic using a single, reliable setup.

---

## ➕ Adding New Tests

To extend the test suite, follow these steps:

### 1. **Pick the Right File**

| If you are testing...  | Add your test to...  |
| ---------------------- | -------------------- |
| `Sorter` class logic   | `test_sorter.py`     |
| `FileUtils` or helpers | `test_file_utils.py` |
| New shared fixtures    | `conftest.py`        |

### 2. **Write a Test Function**

Create a new function starting with `test_`. Use the `file_tree` fixture or create a new one if a different structure is needed.

```python
# In test_sorter.py
def test_new_feature_moves_files(sorter_instance, file_tree):
    # 1. Call the function you are testing
    sorter_instance.new_feature(str(file_tree))

    # 2. Assert that the outcome is what you expect
    assert (file_tree / "New_Category" / "script.py").is_file()
    assert not (file_tree / "script.py").exists()
```

### 3. **Create a Fixture (If Needed)**

If your test requires a unique file structure, add a new fixture in `conftest.py`.

```python
# In conftest.py
@pytest.fixture
def custom_tree(tmp_path):
    (tmp_path / "file-01.log").touch()
    (tmp_path / "file-02.log").touch()
    return tmp_path
```

---

## Running the Tests

First, ensure you have `pytest` and `pytest-cov` (for coverage reporting) installed:

```bash
pip install pytest pytest-cov
```

From the root directory of the project, run one of the following commands:

**Run all tests:**

```bash
pytest
```

**Run tests with a coverage report:**

```bash
pytest --cov=sortium
```

---

## Additional Notes

All tests are designed to be completely isolated. They operate exclusively within temporary directories created and automatically destroyed by `pytest`, ensuring that no changes are made to your actual file system.
