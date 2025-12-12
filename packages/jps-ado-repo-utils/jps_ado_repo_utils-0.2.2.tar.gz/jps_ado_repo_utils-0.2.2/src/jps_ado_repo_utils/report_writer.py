from __future__ import annotations

import getpass
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_duration(start: datetime, end: datetime) -> str:
    total = int((end - start).total_seconds())
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def section_banner(number: int, description: str) -> str:
    return (
        "##--------------------------------------------------------------\n"
        "##\n"
        f"## Section {number}: {description}\n"
        "##\n"
        "#--------------------------------------------------------------\n"
    )


def write_full_report(
    report_file: Path,
    infile: Path,
    outdir: Path,
    logfile: Path,
    start_time: datetime,
    end_time: datetime,
    clone_failures,
    results,
    scan_failures,
    gitmodule_summary: str,
) -> None:
    """
    Writes the complete RFC1 + RFC2 compliant report file.
    """

    header = [
        f"## method-created: {os.path.abspath(__file__)}",
        f"## date-created: {format_timestamp(datetime.now())}",
        f"## created-by: {getpass.getuser()}",
        f"## logfile: {logfile.resolve()}",
        f"## infile: {infile.resolve()}",
        f"## outdir: {outdir.resolve()}",
        f"## start-time: {format_timestamp(start_time)}",
        f"## end-time: {format_timestamp(end_time)}",
        f"## duration: {format_duration(start_time, end_time)}",
        "",
    ]

    lines = []
    lines.extend(header)

    section_num = 1

    # 1. Failed Clones
    lines.append(section_banner(section_num, "Failed Git Clone"))
    section_num += 1
    if not clone_failures:
        lines.append("(none)\n")
    else:
        for f in clone_failures:
            lines.append(f"{f.repo_url}")
            lines.append(f"  Error: {f.error_message}\n")

    # 2. Scanned Repositories
    lines.append(section_banner(section_num, "Scanned Repositories"))
    section_num += 1
    if not results:
        lines.append("(none)\n")
    else:
        for r in results:
            lines.append(str(r.local_path.resolve()))
        lines.append("")

    # 3. Git Modules
    lines.append(section_banner(section_num, "Detected Git Submodules"))
    section_num += 1
    lines.append(gitmodule_summary + "\n")

    # 4. Repositories with Found Dependency
    found = [r for r in results if r.found_dependency]
    lines.append(section_banner(section_num, "Found Dependency"))
    section_num += 1
    if not found:
        lines.append("(none)\n")
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
                for pf in r.python_files_with_import:
                    lines.append(f"    {pf.resolve()}")
            else:
                lines.append("    (none)")
            lines.append("")

    # 5. Repositories without Dependency
    not_found = [r for r in results if not r.found_dependency]
    lines.append(section_banner(section_num, "Dependency Not Found"))
    section_num += 1

    if not not_found:
        lines.append("(none)\n")
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

    # 6. Scan Errors
    lines.append(section_banner(section_num, "Scan Errors"))
    if not scan_failures:
        lines.append("(none)\n")
    else:
        for f in scan_failures:
            lines.append(f"{f.repo_url}")
            if f.local_path:
                lines.append(f"  Local path: {f.local_path.resolve()}")
            lines.append(f"  Error: {f.error_message}\n")

    report_file.write_text("\n".join(lines), encoding="utf-8")
