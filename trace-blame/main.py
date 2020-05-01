import os
from sys import exc_info

from git import Repo

# override me
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Blame:
    def __init__(self, last_commit):
        self.name = last_commit.author.name
        self.email = last_commit.author.email
        self.message = last_commit.message
        self.commit_with_branch_or_first_tag = last_commit.name_rev
        self.date = last_commit.committed_datetime.isoformat()

    def __repr__(self):
        return repr(self.__dict__)


class ExtendedRepo(Repo):
    @property
    def files_in_repo(self):
        return self.git.ls_tree("--name-only", r=self.head.ref.name).split()

    @property
    def full_path_files_in_repo(self):
        return [os.path.join(self.working_dir, path) for path in self.files_in_repo]

    def get_blame_repr(self, path, line):
        if path not in self.full_path_files_in_repo:
            return None

        last_commit = self.blame('HEAD', path, L=line)[0][0]
        return Blame(last_commit=last_commit)


def get_last_commit_data(path, line):
    if not hasattr(get_last_commit_data, '_repo'):
        get_last_commit_data._repo = ExtendedRepo(BASE_DIR)

    return get_last_commit_data._repo.get_blame_repr(path=path, line=line)


def iter_stacks(tb):
    tb_ = tb

    while tb_ is not None:
        yield tb_
        tb_ = tb_.tb_next


def exc_info_with_blame():
    exc_type, exc_value, exc_traceback = exc_info()
    for tb in iter_stacks(exc_traceback):
        tb.tb_frame.f_locals.update(
            {"blame": get_last_commit_data(path=tb.tb_frame.f_code.co_filename, line=tb.tb_lineno)}
        )
    return exc_type, exc_value, exc_traceback
