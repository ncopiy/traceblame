import os

from git import Repo

from traceblame import TracebackExtender


TRACEBLAME_GIT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_current_tb_extender() -> TracebackExtender:
    repo = Repo(path=TRACEBLAME_GIT_PATH)
    return TracebackExtender(repo=repo)
