import os

from git import Repo

from traceblame import TracebackExtender


def divide_by_zero():
    return 10 / 0


DIVIDE_TO_ZERO_LINE = 9
TRACEBLAME_GIT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALL_FILES_IN_TRACEBLAME_REPO = {
    '.github/workflows/pipeline.yml',
    '.github/workflows/release.yml',
    '.gitignore',
    'traceblame/main.py',
    'traceblame/__init__.py',
    'requirements.txt',
    'tests/__init__.py',
    'tests/tests.py',
    'tests/utils.py',
    'setup/__init__.py',
    'setup/setup.py',
    'LICENSE',
    'README.md',
}


def get_current_tb_extender() -> TracebackExtender:
    repo = Repo(path=TRACEBLAME_GIT_PATH)
    return TracebackExtender(repo=repo)
