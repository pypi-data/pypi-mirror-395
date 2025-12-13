import os


class GitService:
    def _call_os(self, command: str) -> str:
        return os.popen(command).read()

    def get_diff(self, path: str, start_commit: str, end_commit: str) -> str:
        os.chdir(path)
        return self._call_os(f"git diff {start_commit} {end_commit}")

    def clone(self, repo_url: str, clone_path: str) -> None:
        self._call_os(f"git clone {repo_url} {clone_path}")
