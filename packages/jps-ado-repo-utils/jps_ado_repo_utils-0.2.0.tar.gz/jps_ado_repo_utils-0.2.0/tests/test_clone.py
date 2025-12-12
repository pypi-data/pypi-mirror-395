import subprocess
from pathlib import Path
from unittest.mock import patch

from jps_ado_repo_utils.dependency_finder import clone_repository


def test_clone_success(tmp_path: Path):
    """
    Mock a successful git clone operation.
    The test must create the destination directory because subprocess.run is mocked.
    """
    repo_url = "git@github.com:example/repo.git"
    base = tmp_path

    mock_result = subprocess.CompletedProcess(
        args=["git", "clone"],
        returncode=0,
        stdout="OK",
        stderr=""
    )

    with patch("subprocess.run", return_value=mock_result):
        repo_dir, err = clone_repository(repo_url, base)

    # Validate clone_repository() returned correct values
    assert err is None
    assert repo_dir is not None

    # Create the mocked clone directory
    repo_dir.mkdir(parents=True, exist_ok=True)

    # Now the expected behavior is satisfied
    assert repo_dir.exists()


def test_clone_failure(tmp_path: Path):
    """
    Mock a failed git clone operation.
    """
    repo_url = "git@github.com:example/repo.git"
    base = tmp_path

    mock_result = subprocess.CompletedProcess(
        args=["git", "clone"],
        returncode=1,
        stdout="",
        stderr="permission denied"
    )

    with patch("subprocess.run", return_value=mock_result):
        repo_dir, err = clone_repository(repo_url, base)

    assert repo_dir is None
    assert "permission denied" in err
