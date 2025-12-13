import subprocess
import re

from abc import ABC, abstractmethod
from enum import StrEnum
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from logging import getLogger
from pathlib import Path
from shutil import rmtree
from typing import Iterator

from sqlalchemy.sql.expression import select

from phystool.config import config
from phystool.helper import terminal_yes_no, silent_keyboard_interrupt
from phystool.physql import physql_db
from phystool.physql.models import PDBRecord

logger = getLogger(__name__)


class PhysGitError(Exception):
    pass


class GitFile(ABC):
    SUFFIXES: list[str]
    IN_DIR: Path

    class Status(StrEnum):
        MODIFIED = "M"
        MODIFIED_SUBMODULE = "m"
        ADDED = "A"
        ADDED_AND_MODIFIED = "AM"
        DELETED = "D"
        RENAMED = "R"
        COPIED = "C"
        UNTRACKED = "??"
        IGNORED = "!!"

    def __init__(self, status: Status, path: Path):
        self._files = {suffix[1:]: "" for suffix in self.SUFFIXES}
        self.n = 0
        self.uuid = path.stem
        self.status = status
        self.title = ""
        self.add(path)

    @classmethod
    def create(cls, status: Status, path: Path) -> "GitFile":
        if path.suffix in GitPDBFile.SUFFIXES:
            return GitPDBFile(status, path)
        if path.name in GitExtraFile.FILES:
            return GitExtraFile(status, path)
        if path.suffix in GitTexFile.SUFFIXES:
            return GitTexFile(status, path)
        raise ValueError

    @abstractmethod
    def add(self, path: Path) -> None: ...

    def message(self) -> str:
        exts = "/".join([suffix for suffix, path in self._files.items() if path])
        return f"{self.status.name[0]}: {self.uuid} {exts}"

    def _commands(self) -> Iterator[str]:
        for path in self._files.values():
            if path:
                match self.status:
                    case self.Status.ADDED | self.Status.UNTRACKED:
                        yield f"bat --color always {path}"
                    case self.Status.MODIFIED | self.Status.ADDED_AND_MODIFIED:
                        yield f"git diff {path} | delta {config.DELTA_THEME}"
                    case self.Status.DELETED:
                        yield f"git show HEAD:{path} | bat --color always"
                    case _:
                        raise PhysGitError(f"Unexpected status {self.status}")

    def get_files(self) -> list[str]:
        return [f for f in self._files.values() if f]

    def get_diff(self) -> str:
        out = ""
        for cmd in self._commands():
            tmp = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                cwd=config.db.DB_DIR,
            )
            if tmp.returncode == 0:
                out += tmp.stdout
            else:
                logger.warning(f"git diff failed ({tmp.returncode})")
                logger.warning(tmp.stderr)
        return out

    def display_diff(self) -> None:
        for cmd in self._commands():
            subprocess.run(cmd, shell=True, cwd=config.db.DB_DIR)


class GitPDBFile(GitFile):
    SUFFIXES = [".tex", ".json", ".py", ".pty"]

    def _get_title(self, uuid: str) -> str:
        if not hasattr(self, "_pdb_record_map"):
            with physql_db() as session:
                self._pdb_record_map = {
                    str(uuid): title
                    for uuid, title in session.execute(
                        select(PDBRecord.uuid, PDBRecord.title)
                    )
                }
        return self._pdb_record_map.get(uuid, str(uuid))

    def add(self, path: Path) -> None:
        if (
            self.status != self.Status.DELETED
            and not (config.db.DB_DIR / path.name).exists()
        ):
            raise ValueError

        if path.stem != self.uuid:
            logger.error(f"Non matching uuids ({path.stem} != {self.uuid})")
            raise PhysGitError(f"{path.stem} != {self.uuid}")

        self.n += 1
        self._files[path.suffix[1:]] = str(path)
        self.title = self._get_title(self.uuid)


class GitTexFile(GitFile):
    SUFFIXES = [".sty", ".cls"]

    def add(self, path: Path) -> None:
        if (
            self.status != self.Status.DELETED
            and not (config.db.PHYSTEX / path.name).exists()
        ):
            raise ValueError

        self._files[path.suffix[1:]] = str(path)
        self.title = path.name
        if not self.n:
            self.n += 1
        else:
            raise PhysGitError(f"Multiple GitTexFile with same name: {path}")


class GitExtraFile(GitFile):
    SUFFIXES = [".conf"]
    FILES = ["0_physdb.conf", ".gitignore"]

    def add(self, path: Path) -> None:
        if (
            self.status != self.Status.DELETED
            and not (config.db.DB_DIR / path.name).exists()
        ):
            raise ValueError

        if path.name != ".gitignore" and path.suffix != ".conf":
            raise PhysGitError(f"Unsupported hidden file {path}")

        self._files[path.suffix[1:]] = str(path)
        self.title = path.name
        if not self.n:
            self.n += 1
        else:
            raise PhysGitError(f"Multiple GitHiddenFile with same name: {path}")


class PhysGit:
    def __init__(self) -> None:
        """
        Helper class to manage PDBFile stored in config.DB_DIR. If the
        directory is not a valid git repository it raises
        InvalidGitRepositoryError.

        To have a nicer git diff experience, this helper class uses bat and
        delta (named git-delta in debian package manager).
        """
        self._repo = Repo(config.db.DB_DIR)
        self._staged: dict[GitFile.Status, list[GitFile]] = {
            status: [] for status in GitFile.Status
        }
        self._git_map: dict[str, GitFile] = {}

        for line in self._repo.git.status(short=True).splitlines():
            try:
                status_letter, fname = line.strip().split()
            except ValueError:
                logger.error(
                    f"Can't handle: {line}.\n"
                    "Running the appropriate git commands should fix the problem."
                )
                continue

            status = GitFile.Status(status_letter)
            path = Path(fname)
            if status in (
                GitFile.Status.ADDED,
                GitFile.Status.ADDED_AND_MODIFIED,
                GitFile.Status.DELETED,
                GitFile.Status.MODIFIED,
                GitFile.Status.UNTRACKED,
            ):
                if gpdb := self._git_map.get(path.stem, None):
                    gpdb.add(path)
                else:
                    try:
                        self._git_map[path.stem] = GitFile.create(status, path)
                    except ValueError:
                        logger.info(f"Not managed by phystool: {path} ({status})")
            elif status == GitFile.Status.MODIFIED_SUBMODULE:
                logger.info(f"Do nothing for submodule: {path} ({status})")
            else:
                raise PhysGitError(f"Don't know how to handle {path} ({status})")

    def __len__(self) -> int:
        return len(self._git_map)

    def __getitem__(self, uuid: str) -> GitFile:
        return self._git_map[uuid]

    def __iter__(self) -> Iterator[GitFile]:
        return iter(self._git_map.values())

    def _get_git_message(self) -> str:
        return "{}\n\n{}".format(
            ", ".join(
                [
                    f"{len(list_staged)} ({sum(git_file.n for git_file in list_staged)}) {status.name}"
                    for status, list_staged in self._staged.items()
                    if list_staged
                ]
            ),
            "\n".join(
                git_file.message()
                for list_staged in self._staged.values()
                for git_file in list_staged
            ),
        )

    @silent_keyboard_interrupt
    def interactive_staging(self) -> None:
        by_status: dict[GitFile.Status, list[GitFile]] = {
            status: [] for status in GitFile.Status
        }
        maxlen = 0
        for git_pdb_file in self:
            by_status[git_pdb_file.status].append(git_pdb_file)
            if len(git_pdb_file.title) > maxlen:
                maxlen = len(git_pdb_file.title)

        for status, list_sorted in by_status.items():
            for git_pdb_file in list_sorted:
                git_pdb_file.display_diff()
                if terminal_yes_no(
                    f"{git_pdb_file.title: <{maxlen}} -> stage {status.name}?"
                ):
                    self.stage(git_pdb_file)

    def stage(self, git_pdb_file: GitFile) -> None:
        self._staged[git_pdb_file.status].append(git_pdb_file)

    def commit(self, for_terminal: bool) -> str:
        if not any(self._staged.values()):
            msg = "Nothing was staged, git is left untouched"
            logger.info(msg)
            return msg

        git_msg = self._get_git_message()
        logger.info("Review Git actions")
        logger.info(git_msg)
        if for_terminal and not terminal_yes_no("Commit those changes?"):
            return "Commit cancelled by user"

        for git_pdb_file in self._staged[GitFile.Status.UNTRACKED]:
            self._repo.index.add(git_pdb_file.get_files())
        for git_pdb_file in self._staged[GitFile.Status.MODIFIED]:
            self._repo.index.add(git_pdb_file.get_files())
        for git_pdb_file in self._staged[GitFile.Status.DELETED]:
            self._repo.index.remove(git_pdb_file.get_files())

        self._repo.index.commit(git_msg)

        try:
            origin = self._repo.remote()
            push_info = origin.push()
            push_info.raise_if_error()
            msg = "Push successful"
            logger.info(msg)
            return msg
        except GitCommandError as e:
            if e.status == 128:
                msg = "Push failed (no internet)"
            else:
                msg = "Push failed (unknown error)"
                logger.error(e)
        except ValueError:
            msg = "Push failed (no remote found)"
        raise PhysGitError(msg)

    def get_remote_url(self) -> str:
        return self._repo.remote().url


@silent_keyboard_interrupt
def run_git_in_terminal() -> None:
    try:
        git = PhysGit()
        git.interactive_staging()
        git.commit(for_terminal=True)
    except InvalidGitRepositoryError:
        print("The database is not managed by git.")
        setup_git_repository(input("Enter url of remote git repository: "))
    except PhysGitError as e:
        logger.exception(e)


def is_valid_git_remote(remote_url: str) -> bool:
    return bool(re.match("git@(.*):(.*).git", remote_url))


def setup_git_repository(remote_url: str) -> None:
    """
    Initialize the local git repository and link it to its remote.

    :remote_url: url of an empty remote repository
    """
    if is_valid_git_remote(remote_url):
        raise InvalidGitRepositoryError("The url is not formatted correctly.")

    err_msg = ""
    repo = Repo.init(config.db.DB_DIR)
    repo.create_remote("origin", remote_url)
    try:
        if repo.git.ls_remote():
            err_msg = "The remote is not empty."
    except GitCommandError as e:
        if e.status == 128:
            err_msg = "The remote can't be found."
        else:
            err_msg = str(e)
    except Exception as e:
        err_msg = str(e)

    if err_msg:
        rmtree(repo.git_dir)
        raise InvalidGitRepositoryError(err_msg)

    gitignore = config.db.DB_DIR / ".gitignore"
    with gitignore.open("wt") as gf:
        gf.write("\n".join(["0_metadata.pkl", "/*.pdf"]))
    repo.index.add([str(gitignore)])

    repo.index.commit("initial commit: setup gitconfig")
    repo.git.add(update=True)
    repo.git.push("--set-upstream", "origin", "master")
    repo.remote("origin").push()
    logger.info("The git repository was correctly initialized")


def clone_git_repository(remote_url: str, to_path: Path):
    try:
        Repo.clone_from(remote_url, to_path)
    except GitCommandError as e:
        logger.error(e)
