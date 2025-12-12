#!/usr/bin/env python3
from __future__ import annotations

"""
Constants for the dependency_finder tool.

All default values for the program are centralized here.
"""

import os
from pathlib import Path

# Base temp directory for all output
DEFAULT_TMP_DIR: Path = Path("/tmp")

# Tool namespace component under the user directory
TOOL_ROOT_DIR_NAME: str = "jps-ado-repo-utils"

# Timestamp format used in directory naming
TIMESTAMP_FORMAT: str = "%Y-%m-%d-%H%M%S"

# Default filenames
REPORT_FILENAME: str = "report.txt"
LOGFILE_SUFFIX: str = ".log"

# Default project configuration files to scan for dependencies
DEFAULT_PROJECT_FILE_NAMES: tuple[str, ...] = (
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "setup.cfg",
)

# Default maximum number of worker threads
DEFAULT_MAX_WORKERS: int = min(32, os.cpu_count() or 4)

# Section titles for the report file
FAILED_GIT_CLONE_SECTION_TITLE: str = "Failed Git Clone"
SCANNED_REPOSITORIES_SECTION_TITLE: str = "Scanned Repositories"
FOUND_DEPENDENCY_SECTION_TITLE: str = "Found Dependency"
DEPENDENCY_NOT_FOUND_SECTION_TITLE: str = "Dependency Not Found"
SCAN_ERRORS_SECTION_TITLE: str = "Scan Errors"
