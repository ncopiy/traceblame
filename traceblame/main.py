from __future__ import annotations

import os
from sys import exc_info
from types import TracebackType
from typing import List, Optional, Iterable, Tuple, Type

from git import Repo, Commit


__names__ = [
    'Blame',
    'TracebackExtender',
    'iter_stacks',
]


class Blame:
    def __init__(self, last_commit: Commit):
        self.name = last_commit.author.name
        self.email = last_commit.author.email
        self.message = last_commit.message
        self.commit = last_commit.hexsha
        self.commit_with_branch_or_first_tag = last_commit.name_rev
        self.date = last_commit.committed_datetime.isoformat()

    def __repr__(self):
        return repr(self.__dict__)


class TracebackEnricher:
    def __init__(self, repo: Repo, *args, **kwargs):
        self.repo = repo

    @property
    def files_in_repo(self) -> List[str]:
        """
        Returns list of related files paths existed in git repository
        """
        return self.repo.git.ls_files().split()

    @property
    def full_path_files_in_repo(self) -> List[str]:
        """
        Returns list of full files paths existed in git repository
        """
        return [os.path.join(self.repo.working_dir, path) for path in self.files_in_repo]

    def get_blame_repr(self, path: str, line: int) -> Optional[Blame]:
        """
        Returns if possible Blame object with commit info based on provided line and path
        """
        last_commit = self.get_last_commit(path=path, line=line)
        return None if last_commit is None else Blame(last_commit=last_commit)

    def get_last_commit(self, path: str, line: int) -> Optional[Commit]:
        """
        Returns if possible last commit object based on provided line and path
        """
        if path not in self.full_path_files_in_repo:
            return None

        try:
            return self.repo.blame(rev='HEAD', file=path, incremental=False, L=line)[0][0]
        except IndexError:
            return None

    def get_extended_exc_info(self) -> Tuple[Type[BaseException], BaseException, TracebackType]:
        """
        This function acts like sys.exc_info() but with blame data in traceback object
        """
        exc_type, exc_value, exc_traceback = exc_info()
        exc_traceback = self.get_extended_traceback(exc_traceback)
        return exc_type, exc_value, exc_traceback

    def get_extended_traceback(self, traceback: TracebackType) -> TracebackType:
        """
        Extends provided traceback object by blame info if possible
        """
        for tb in iter_stacks(traceback):
            tb.tb_frame.f_locals.update(
                {"blame": self.get_blame_repr(path=tb.tb_frame.f_code.co_filename, line=tb.tb_lineno)}
            )
        return traceback


def iter_stacks(tb: Optional[TracebackType]) -> Iterable[TracebackType]:
    tb_ = tb

    while tb_ is not None:
        yield tb_
        tb_ = tb_.tb_next
