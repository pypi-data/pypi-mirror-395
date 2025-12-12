#!/usr/bin/env python3
from __future__ import annotations

"""
dependency_finder.py

Scan multiple git repositories to determine whether a specified Python package
is used as a dependency. The program clones repositories, searches for the
package in selected project configuration files and Python import statements,
and writes a structured report.

Command-line interface is implemented with Typer.
"""

import concurrent.futures
import getpass
import logging
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

import typer

from .constants import (
    DEFAULT_MAX_WORKERS,
    DEFAULT_PROJECT_FILE_NAMES,
    DEFAULT_TMP_DIR,
    DEPENDENCY_NOT_FOUND_SECTION_TITLE,
    FAILED_GIT_CLONE_SECTION_TITLE,
    FOUND_DEPENDENCY_SECTION_TITLE,
    LOGFILE_SUFFIX,
    REPORT_FILENAME,
    SCANNED_REPOSITORIES_SECTION_TITLE,
    SCAN_ERRORS_SECTION_TITLE,
    TIMESTAMP_FORMAT,
    TOOL_ROOT_DIR_NAME,
)
from .logger_helper import setup_logging

app = typer.Typer(add_completion=False)


@dataclass
class RepoScanResult:
    """Container for scan results of a single repository.

    Attributes:
        repo_url: The original git repository URL.
        local_path: The local path where the repository was cloned.
        project_files_scanned: List of project configuration files that were scanned.
        project_files_with_dependency: Project files where the dependency was found.
        python_files_scanned: List of Python source files that were scanned.
        python_files_with_import: Python source files where the dependency import was found.
    """

    repo_url: str
    local_path: Path
    project_files_scanned: List[Path] = field(default_factory=list)
    project_files_with_dependency: List[Path] = field(default_factory=list)
    python_files_scanned: List[Path] = field(default_factory=list)
    python_files_with_import: List[Path] = field(default_factory=list)

    @property
    def found_dependency(self) -> bool:
        """Return True if the dependency was found in any project or Python file."""
        return bool(self.project_files_with_dependency or self.python_files_with_import)


@dataclass
class CloneFailure:
    """Information about a failed git clone operation."""

    repo_url: str
    error_message: str


@dataclass
class ScanFailure:
    """Information about a failure during scanning of a repository."""

    repo_url: str
    local_path: Path
    error_message: str


@dataclass
class RepositoryProcessingOutcome:
    """Outcome of processing a single repository (clone + scan)."""

    result: Optional[RepoScanResult] = None
    clone_failure: Optional[CloneFailure] = None
    scan_failure: Optional[ScanFailure] = None


def build_default_paths(
    outdir: Optional[Path],
    logfile: Optional[Path],
    report_file: Optional[Path],
) -> tuple[Path, Path, Path]:
    """Build default outdir, logfile, and report_file paths if not provided.

    Paths follow the pattern:

        base_root = /tmp/{user}/jps-ado-repo-utils/{script_name_without_py}/{YYYY-MM-DD-HHMMSS}/

        outdir      = base_root
        logfile     = base_root / "{script_name_without_py}.log"
        report_file = base_root / "report.txt"

    If the user provides outdir but not logfile or report_file, those files
    are placed inside the provided outdir.

    Args:
        outdir: Optional output directory specified by the user.
        logfile: Optional logfile path specified by the user.
        report_file: Optional report file path specified by the user.

    Returns:
        A tuple of (outdir, logfile, report_file) with all values populated.
    """
    script_name = Path(__file__).stem
    user = getpass.getuser()
    now = datetime.now()
    timestamp = now.strftime(TIMESTAMP_FORMAT)

    if outdir is None:
        base_root = DEFAULT_TMP_DIR / user / TOOL_ROOT_DIR_NAME / script_name / timestamp
        outdir = base_root
    else:
        base_root = outdir

    if logfile is None:
        logfile = base_root / f"{script_name}{LOGFILE_SUFFIX}"

    if report_file is None:
        report_file = base_root / REPORT_FILENAME

    outdir.mkdir(parents=True, exist_ok=True)
    logfile.parent.mkdir(parents=True, exist_ok=True)
    report_file.parent.mkdir(parents=True, exist_ok=True)

    return outdir, logfile, report_file


def read_repo_urls(infile: Path) -> List[str]:
    """Read newline-separated git repository URLs from a file.

    Empty lines and lines that are only whitespace are ignored.

    Args:
        infile: Path to the input file with newline-separated git SSH URLs.

    Returns:
        A list of non-empty, stripped repository URL strings.
    """
    urls: List[str] = []
    with infile.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped:
                urls.append(stripped)
    return urls


def is_ssh_url(repo_url: str) -> bool:
    """Determine whether the given repository URL appears to be an SSH URL.

    Args:
        repo_url: The repository URL string.

    Returns:
        True if the URL looks like an SSH URL, False otherwise.
    """
    if repo_url.startswith("git@"):
        return True
    if repo_url.startswith("ssh://"):
        return True
    if "@vs-ssh." in repo_url:
        return True
    if repo_url.startswith("baylorgenetics@vs-ssh.visualstudio.com"):
        return True
    return False


def slugify_repo_url(repo_url: str) -> str:
    """Create a filesystem-friendly slug from a repository URL.

    Args:
        repo_url: The repository URL.

    Returns:
        A slug that can be safely used as a directory name.
    """
    return re.sub(r"[^A-Za-z0-9._-]", "_", repo_url)


def clone_repository(repo_url: str, base_outdir: Path) -> tuple[Optional[Path], Optional[str]]:
    """Clone a git repository into a subdirectory of the base output directory.

    The subdirectory name is derived from a slugified version of the repo URL.

    Args:
        repo_url: The git repository URL (expected SSH URL).
        base_outdir: Base directory under which the repository will be cloned.

    Returns:
        A tuple of (local_path, error_message). If cloning succeeds, local_path is the
        repository directory and error_message is None. If cloning fails, local_path is
        None and error_message contains a human-readable description.
    """
    slug = slugify_repo_url(repo_url)
    repo_dir = base_outdir / slug

    if repo_dir.exists():
        msg = f"Repository directory already exists, skipping clone: {repo_dir}"
        logging.info(msg)
        return repo_dir, None

    logging.info("Cloning repository '%s' into '%s'", repo_url, repo_dir)

    cmd = ["git", "clone", repo_url, str(repo_dir)]
    try:
        completed = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001
        msg = f"Failed to execute git clone for '{repo_url}': {exc}"
        logging.error(msg)
        return None, msg

    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        msg = (
            f"git clone failed for '{repo_url}' (exit code {completed.returncode}): "
            f"{stderr or 'no error message'}"
        )
        logging.error(msg)
        return None, msg

    logging.info("Successfully cloned repository '%s' into '%s'", repo_url, repo_dir)
    return repo_dir, None


def find_project_files(root: Path) -> List[Path]:
    """Find all project configuration files within a repository.

    Args:
        root: Path to the root of the cloned repository.

    Returns:
        A list of paths to project configuration files to scan.
    """
    matches: List[Path] = []
    for name in DEFAULT_PROJECT_FILE_NAMES:
        for path in root.rglob(name):
            if path.is_file():
                matches.append(path)
    return matches


def find_python_files(root: Path) -> List[Path]:
    """Find all Python source files within a repository.

    Args:
        root: Path to the root of the cloned repository.

    Returns:
        A list of paths to Python source files to scan.
    """
    matches: List[Path] = []
    for path in root.rglob("*.py"):
        if path.is_file():
            matches.append(path)
    return matches


def file_contains_package_string(path: Path, package: str) -> bool:
    """Check whether a file contains the package string anywhere.

    Args:
        path: Path to the file to scan.
        package: The package name to look for.

    Returns:
        True if the file contains the package string, False otherwise.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:  # noqa: PERF203
        logging.warning("Failed to read file '%s': %s", path, exc)
        return False

    return package in text


# def python_file_has_import(path: Path, package: str) -> bool:
#     """Check whether a Python file imports the specified package.

#     This function searches for import statements of the form:

#         import package
#         import package as alias
#         from package import ...
#         from package.submodule import ...

#     Args:
#         path: Path to the Python file.
#         package: The package name to look for.

#     Returns:
#         True if the package is imported in the file, False otherwise.
#     """
#     try:
#         text = path.read_text(encoding="utf-8", errors="ignore")
#     except OSError as exc:  # noqa: PERF203
#         logging.warning("Failed to read Python file '%s': %s", path, exc)
#         return False

#     pattern = re.compile(
#         rf"^\s*(?:from\s+{re.escape(package)}\b|import\s+{re.escape(package)}\b)",
#         re.MULTILINE,
#     )
#     return bool(pattern.search(text))

def python_file_has_import(path: Path, package: str) -> bool:
    """Check whether a Python file imports the specified package.

        import package
        import package as alias
        from package import ...
        from package.submodule import ...

    Args:
        path: Path to the Python file.
        package: The package name to look for.

    Returns:
        True if the package is imported in the file, False otherwise.

    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        logging.warning("Failed to read Python file '%s': %s", path, exc)
        return False

    # Normalize BOM and ensure file ends with newline
    text = text.replace("\ufeff", "") + "\n"

    # More robust line-start matcher:
    # (^|\n) supports BOM, missing newline, and CRLF variations
    pattern = re.compile(
        rf"(^|\n)\s*(?:from\s+{re.escape(package)}\b|import\s+{re.escape(package)}\b)"
    )

    return bool(pattern.search(text))


def scan_repository(repo_url: str, repo_dir: Path, package: str) -> RepoScanResult:
    """Scan a cloned repository for the specified package.

    The repository is scanned for:
      - Presence of the package string in project configuration files.
      - Import statements of the package in Python source files.

    Args:
        repo_url: The original repository URL.
        repo_dir: Local path to the cloned repository.
        package: The package name to search for.

    Returns:
        A RepoScanResult object summarizing the scanning results.
    """
    logging.info("Scanning repository '%s' at '%s'", repo_url, repo_dir)

    result = RepoScanResult(repo_url=repo_url, local_path=repo_dir)

    project_files = find_project_files(repo_dir)
    result.project_files_scanned.extend(project_files)

    for pf in project_files:
        if file_contains_package_string(pf, package):
            result.project_files_with_dependency.append(pf)

    python_files = find_python_files(repo_dir)
    result.python_files_scanned.extend(python_files)

    for py_file in python_files:
        if python_file_has_import(py_file, package):
            result.python_files_with_import.append(py_file)

    logging.info(
        "Completed scanning repository '%s'. Dependency found: %s",
        repo_url,
        result.found_dependency,
    )

    return result


def process_repository(
    repo_url: str,
    base_outdir: Path,
    package: str,
) -> RepositoryProcessingOutcome:
    """Clone and scan a single repository.

    Args:
        repo_url: The git repository URL.
        base_outdir: Base output directory where repositories will be cloned.
        package: The package name to search for.

    Returns:
        A RepositoryProcessingOutcome summarizing clone/scan results.
    """
    if not is_ssh_url(repo_url):
        msg = "Non-SSH URL detected; treating as failed git clone."
        logging.error("%s URL: %s", msg, repo_url)
        return RepositoryProcessingOutcome(
            clone_failure=CloneFailure(repo_url=repo_url, error_message=msg),
        )

    repo_dir, clone_error = clone_repository(repo_url, base_outdir)
    if repo_dir is None:
        return RepositoryProcessingOutcome(
            clone_failure=CloneFailure(
                repo_url=repo_url,
                error_message=clone_error or "git clone failed with unknown error",
            ),
        )

    try:
        result = scan_repository(repo_url, repo_dir, package)
    except Exception as exc:  # noqa: BLE001
        msg = f"Exception while scanning repository '{repo_url}' at '{repo_dir}': {exc}"
        logging.error(msg)
        return RepositoryProcessingOutcome(
            scan_failure=ScanFailure(
                repo_url=repo_url,
                local_path=repo_dir,
                error_message=str(exc),
            ),
        )

    return RepositoryProcessingOutcome(result=result)


def write_report(
    report_file: Path,
    results: Sequence[RepoScanResult],
    clone_failures: Sequence[CloneFailure],
    scan_failures: Sequence[ScanFailure],
) -> None:
    """Write the report file with the required sections.

    Sections:
      1. Failed Git Clone
         - repo URL
         - error message

      2. Scanned Repositories
         - newline-separated list of local repository paths.

      3. Found Dependency
         - for each repo where the package was found:
           - local repo path
           - "Project files with dependency:" list
           - "Python files with import:" list

      4. Dependency Not Found
         - for each repo where the package was not found:
           - local repo path
           - "Project files scanned:" list
           - "Python files scanned:" list

      5. Scan Errors
         - for each repository with a scan error:
           - repo URL
           - local path
           - error message

    Args:
        report_file: Path to the report file to write.
        results: Successful scan results.
        clone_failures: Clone failure details.
        scan_failures: Scan failure details.
    """
    logging.info("Writing report to '%s'", report_file)

    found: List[RepoScanResult] = [r for r in results if r.found_dependency]
    not_found: List[RepoScanResult] = [r for r in results if not r.found_dependency]

    lines: List[str] = []

    # Section: Failed Git Clone
    lines.append(FAILED_GIT_CLONE_SECTION_TITLE)
    lines.append("=" * len(FAILED_GIT_CLONE_SECTION_TITLE))
    if not clone_failures:
        lines.append("(none)")
    else:
        for failure in clone_failures:
            lines.append(failure.repo_url)
            lines.append(f"  Error: {failure.error_message}")
            lines.append("")
    lines.append("")

    # Section: Scanned Repositories
    lines.append(SCANNED_REPOSITORIES_SECTION_TITLE)
    lines.append("=" * len(SCANNED_REPOSITORIES_SECTION_TITLE))
    if not results:
        lines.append("(none)")
    else:
        for r in results:
            lines.append(str(r.local_path.resolve()))
    lines.append("")

    # Section: Found Dependency
    lines.append(FOUND_DEPENDENCY_SECTION_TITLE)
    lines.append("=" * len(FOUND_DEPENDENCY_SECTION_TITLE))
    if not found:
        lines.append("(none)")
    else:
        for r in found:
            lines.append(str(r.local_path.resolve()))
            lines.append("  Project files with dependency:")
            if r.project_files_with_dependency:
                for pf in r.project_files_with_dependency:
                    lines.append(f"    {pf.resolve()}")
            else:
                lines.append("    (none)")

            lines.append("  Python files with import:")
            if r.python_files_with_import:
                for py in r.python_files_with_import:
                    lines.append(f"    {py.resolve()}")
            else:
                lines.append("    (none)")
            lines.append("")
    lines.append("")

    # Section: Dependency Not Found
    lines.append(DEPENDENCY_NOT_FOUND_SECTION_TITLE)
    lines.append("=" * len(DEPENDENCY_NOT_FOUND_SECTION_TITLE))
    if not not_found:
        lines.append("(none)")
    else:
        for r in not_found:
            lines.append(str(r.local_path.resolve()))
            lines.append("  Project files scanned:")
            if r.project_files_scanned:
                for pf in r.project_files_scanned:
                    lines.append(f"    {pf.resolve()}")
            else:
                lines.append("    (none)")

            lines.append("  Python files scanned:")
            if r.python_files_scanned:
                for py in r.python_files_scanned:
                    lines.append(f"    {py.resolve()}")
            else:
                lines.append("    (none)")
            lines.append("")
    lines.append("")

    # Section: Scan Errors
    lines.append(SCAN_ERRORS_SECTION_TITLE)
    lines.append("=" * len(SCAN_ERRORS_SECTION_TITLE))
    if not scan_failures:
        lines.append("(none)")
    else:
        for failure in scan_failures:
            lines.append(failure.repo_url)
            if failure.local_path:
                lines.append(f"  Local path: {failure.local_path.resolve()}")
            lines.append(f"  Error: {failure.error_message}")
            lines.append("")
    lines.append("")

    report_file.write_text("\n".join(lines), encoding="utf-8")
    logging.info("Report successfully written to '%s'", report_file)


@app.command()
def main(  # noqa: D417
    infile: Path = typer.Option(
        ...,
        "--infile",
        "-i",
        exists=True,
        readable=True,
        resolve_path=True,
        help="Input file containing newline-separated git repository SSH URLs.",
    ),
    package: str = typer.Option(
        ...,
        "--package",
        "-p",
        help='Package name to scan for (e.g., "pipeline-api-endpoints").',
    ),
    outdir: Optional[Path] = typer.Option(
        None,
        "--outdir",
        "-o",
        resolve_path=True,
        help=(
            "Output directory for cloned repositories and report. "
            "Defaults to /tmp/{user}/jps-ado-repo-utils/{script_name}/{timestamp}/"
        ),
    ),
    logfile: Optional[Path] = typer.Option(
        None,
        "--logfile",
        "-l",
        resolve_path=True,
        help=(
            "Log file path. Defaults to "
            "/tmp/{user}/jps-ado-repo-utils/{script_name}/{timestamp}/{script_name}.log "
            "or inside the provided outdir."
        ),
    ),
    report_file: Optional[Path] = typer.Option(
        None,
        "--report-file",
        "-r",
        resolve_path=True,
        help=(
            "Report file path. Defaults to "
            "/tmp/{user}/jps-ado-repo-utils/{script_name}/{timestamp}/report.txt "
            "or inside the provided outdir."
        ),
    ),
    max_workers: Optional[int] = typer.Option(
        None,
        "--max-workers",
        "-w",
        min=1,
        help=(
            "Maximum number of worker threads to use for cloning and scanning. "
            "Defaults to a dynamic value based on available CPUs."
        ),
    ),
) -> None:
    """Find repositories that depend on a given Python package.

    This command reads a list of git repository URLs from an input file, clones
    each repository into an output directory, and scans project configuration
    files and Python source files for usage of the specified package. It writes
    a report summarizing which repositories depend on the package.

    Args:
        infile: Path to the input file containing newline-separated repository URLs.
        package: Name of the Python package to search for.
        outdir: Optional output directory for cloned repositories and report.
        logfile: Optional path to the log file.
        report_file: Optional path to the report file.
        max_workers: Optional maximum number of worker threads.
    """
    outdir, logfile, report_file = build_default_paths(outdir, logfile, report_file)
    setup_logging(logfile)

    logging.info("Starting dependency_finder execution.")
    logging.info("Input file: %s", infile)
    logging.info("Package to search for: %s", package)
    logging.info("Output directory: %s", outdir)
    logging.info("Log file: %s", logfile)
    logging.info("Report file: %s", report_file)

    repo_urls = read_repo_urls(infile)
    if not repo_urls:
        logging.warning("No repository URLs found in input file '%s'.", infile)
        write_report(report_file, [], [], [])
        print(f"Wrote the log file to '{logfile.resolve()}'")
        print(f"Wrote the report file to '{report_file.resolve()}'")
        return

    effective_max_workers = max_workers or DEFAULT_MAX_WORKERS
    logging.info("Using up to %s worker threads for cloning and scanning.", effective_max_workers)

    results: List[RepoScanResult] = []
    clone_failures: List[CloneFailure] = []
    scan_failures: List[ScanFailure] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=effective_max_workers) as executor:
        future_to_url = {
            executor.submit(process_repository, url, outdir, package): url
            for url in repo_urls
        }

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                outcome = future.result()
            except Exception as exc:  # noqa: BLE001
                msg = f"Unhandled exception while processing repository '{url}': {exc}"
                logging.error(msg)
                scan_failures.append(
                    ScanFailure(
                        repo_url=url,
                        local_path=Path(),
                        error_message=str(exc),
                    ),
                )
                continue

            if outcome.clone_failure is not None:
                clone_failures.append(outcome.clone_failure)
            if outcome.scan_failure is not None:
                scan_failures.append(outcome.scan_failure)
            if outcome.result is not None:
                results.append(outcome.result)

    write_report(report_file, results, clone_failures, scan_failures)

    logging.info("Finished dependency_finder execution.")

    print(f"Wrote the log file to '{logfile.resolve()}'")
    print(f"Wrote the report file to '{report_file.resolve()}'")


if __name__ == "__main__":
    app()
