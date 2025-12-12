from typing import Dict, List, Set

DEFAULT_FILE_TYPES: Dict[str, List[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp", ".key"],
    "Videos": [".mp4", ".avi", ".mov", ".wmv", ".mkv", ".flv", ".webm"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [
        ".py",
        ".js",
        ".html",
        ".css",
        ".java",
        ".cpp",
        ".c",
        ".ts",
        ".json",
        ".xml",
        ".sql",
    ],
    "Executables": [".exe", ".msi", ".apk", ".bat", ".sh", ".bin"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Design": [".psd", ".ai", ".xd", ".sketch", ".fig"],
    "Others": [],
}

"""Default file type categories and their associated file extensions.

Used to map file extensions to logical categories during file sorting.

Examples:
    >>> DEFAULT_FILE_TYPES["Images"]
    ['.jpg', '.jpeg', '.png', '.gif']

Categories include:
    - Images
    - Documents
    - Spreadsheets
    - Presentations
    - Videos
    - Music
    - Archives
    - Code
    - Executables
    - Fonts
    - Design
    - Others
"""


DEFAULT_IGNORE_ENTRIES: Set[str] = {
     ".git",
     ".gitignore",
     ".gitattributes",
     ".gitmodules",
     ".DS_Store",
     "__pycache__",
     "node_modules",
     ".venv",
     "venv",
     ".idea",
     ".vscode",
     "Thumbs.db",
}

"""Default directory and file names to skip during bulk file operations."""
