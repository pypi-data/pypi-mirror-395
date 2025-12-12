# Sortium

[![PyPI version](https://badge.fury.io/py/sortium.svg?cache-bust=1)](https://badge.fury.io/py/sortium)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Sortium** is a high-performance Python utility for rapidly organizing file systems. It emphasizes a safe, preview-first workflow that lets you plan and review categorized moves (by type, date, or regex) before anything changes on disk.

Designed for both speed and safety, it is memory-efficient for handling massive directories and automatically prevents file overwrites.

---

## Table of Contents

- [Key Features](#key-features)
- [Installation](#installation)
- [Getting Started: Usage Examples](#getting-started-usage-examples)
- [Command Line Usage](#command-line-usage)
- [Running Tests](#running-tests)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

---

## Key Features

- **Plan-first workflow** – Every sort emits an editable JSON plan so you can audit, tweak, version, or share the intended moves before running them.
- **Memory-efficient design** – Uses generators and streaming I/O so it scales to very large trees without exhausting RAM.
- **Flexible sorting strategies** – Built-in helpers for sorting by file type, modification date, or arbitrary regex patterns.
- **Collision-safe moves** – Automatically generates unique destination names (e.g., `image (1).jpg`) to avoid overwriting files.
- **In-place or cross-volume moves** – Choose to tidy a directory in situ or relocate everything into a dedicated archive folder.
- **Utility toolkit** – `FileUtils` exposes recursive scanners, directory flattening, tree export, and reversible plan execution.

---

## Installation

### From PyPI

To install the latest stable version from PyPI:

```bash
pip install sortium
```

### From Source

To install the latest development version from the repository:

```bash
git clone https://github.com/Sarthak-G0yal/Sortium.git
cd Sortium
pip install -e .
```

---

## Getting Started: Usage Examples

Here are a few examples to get you started quickly.

### Example 1: Sort Files by Type

This is the most common use case. It now works in two phases: generate a plan, review/edit the JSON (optional), then apply it when you're ready.

```python
from sortium.sorter import Sorter

# The folder you want to clean up
source_directory = "./my_messy_downloads_folder"

# Create a Sorter instance
sorter = Sorter()

# Phase 1: Generate an editable JSON plan
plan_path = sorter.sort_by_type(
  source_directory,
  recursive=True,  # include nested folders
)

# (Optional) Inspect / edit the JSON plan here
# ...

# Phase 2: Apply the plan when you're satisfied
sorter.file_utils.apply_move_plan(str(plan_path))
print(f"Applied plan {plan_path}")

# Need to undo? Re-use the same plan with reverse=True
sorter.file_utils.apply_move_plan(str(plan_path), reverse=True)

# Prefer a shallow cleanup? Drop recursive=True (it defaults to False).
```

### Example 2: Sort Files to a Different Destination

Organize files from a source folder and move the categorized results to a completely different location.

```python
from sortium.sorter import Sorter

source_dir = "./my_source_files"
destination_dir = "./organized_archive"

sorter = Sorter()

# Generate plan targeted at `destination_dir`
plan_path = sorter.sort_by_type(
  source_dir,
  dest_folder_path=destination_dir,
  plan_output="./sorting_plan.json",
  recursive=True,
)

# Review/edit sorting_plan.json if needed, then execute
sorter.file_utils.apply_move_plan(str(plan_path))
```

### Example 3: Advanced Sorting with Regex

Recursively scan a directory and sort files based on custom patterns. This is great for organizing project files, logs, or datasets.

````python
from sortium.sorter import Sorter

project_folder = "./my_data_science_project"
sorted_output = "./sorted_project_files"

# Define categories and their corresponding regex patterns
regex_map = {
    "Datasets": r".*\.csv$",
    "Notebooks": r".*\.ipynb$",
    "Python_Code": r".*\.py$",
    "Final_Reports": r"final_report_.*\.pdf$"
}

sorter = Sorter()
plan_path = sorter.sort_by_regex(project_folder, regex_map, sorted_output)
sorter.file_utils.apply_move_plan(str(plan_path))
```

---

## Command Line Usage

Sortium now ships with a `sortium` CLI so you can work entirely from the terminal.

```bash
# Generate a recursive type-based plan and write it to Downloads
sortium plan type --source ./Downloads --dest ./Downloads/Sorted --recursive

# Apply or undo the plan later
sortium apply --plan ./Downloads/sortium_plan_type_20250101_101010.json
sortium undo --plan ./Downloads/sortium_plan_type_20250101_101010.json

# Produce a tree snapshot for auditing
sortium tree --source ./Downloads --output ./downloads_structure.json
```

Run `sortium --help` or `sortium plan --help` to explore every flag (strategies,
regex rules, folder-specific date sorting, dry-run previews, etc.).

---

## Running Tests

To run the full test suite and generate a coverage report, first install the development dependencies:

```bash
pip install pytest pytest-cov
````

Then, from the project's root directory, run:

```bash
pytest --cov=sortium
```

For more details on the test structure, see the [Test Suite README](./src/tests/README.md).

---

## Documentation

This project uses [Sphinx](https://www.sphinx-doc.org/) for documentation.

- **Online Documentation**: [**View Documentation**](https://sarthak-g0yal.github.io/Sortium)

- To build the documentation locally:
  ```bash
  # Navigate to the docs directory
  cd docs
  # Install documentation requirements
  pip install -r requirements.txt
  # Build the HTML pages
  make html
  ```
  View the generated files at `docs/_build/html/index.html`.

---

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or fix (`feature/my-feature` or `fix/my-fix`).
3.  Write tests that cover your changes.
4.  Commit your changes using clear, conventional messages.
5.  Open a pull request with a detailed description of your work.

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. Ensure all code is linted and tested before submitting.

- For bugs and feature requests, please [open an issue](https://github.com/Sarthak-G0yal/Sortium/issues).

---

## Author

**Sarthak Goyal**

- Email: [sarthakgoyal487@gmail.com](mailto:sarthakgoyal487@gmail.com)

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
