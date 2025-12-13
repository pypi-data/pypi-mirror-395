from unittest.mock import patch
from app.services.git_service import GitService


def test_get_diff(
    git_service: GitService,
) -> None:
    diff = git_service.get_diff(".", "HEAD", "HEAD~1")
    assert isinstance(diff, str)


def test_clone(
    git_service: GitService,
) -> None:
    repo = "https://github.com/torvalds/linux"
    clone_path = "/tmp/linux_repo"
    with patch.object(git_service, "_call_os") as mock_call_os:
        git_service.clone(repo, clone_path)
        mock_call_os.assert_called_once_with(f"git clone {repo} {clone_path}")
