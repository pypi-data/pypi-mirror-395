from jps_ado_repo_utils.dependency_finder import scan_repository


def test_scan_finds_project_dependency(repo_with_dependency):
    """Verify that scanner detects dependency inside project file."""
    result = scan_repository(
        repo_url="git@fake/repo1.git",
        repo_dir=repo_with_dependency,
        package="mypkg"
    )

    assert result.found_dependency
    assert any("pyproject.toml" in str(p) for p in result.project_files_with_dependency)


def test_scan_detects_import_only(repo_with_import_only):
    """Verify that scanner detects Python import usage."""
    result = scan_repository(
        repo_url="git@fake/repo2.git",
        repo_dir=repo_with_import_only,
        package="mypkg"
    )

    assert result.found_dependency
    assert len(result.python_files_with_import) > 0
    assert any("main.py" in str(p) for p in result.python_files_with_import)


def test_scan_no_dependency(repo_without_dependency):
    """Verify that scanner correctly reports no dependency."""
    result = scan_repository(
        repo_url="git@fake/repo3.git",
        repo_dir=repo_without_dependency,
        package="mypkg"
    )

    assert not result.found_dependency
    assert len(result.python_files_with_import) == 0
    assert len(result.project_files_with_dependency) == 0
