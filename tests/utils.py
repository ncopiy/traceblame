import os

from git import Repo

from traceblame import TracebackExtender


def divide_by_zero():
    return 10 / 0


def divide_by_zero_caller():
    divide_by_zero()


DIVIDE_TO_ZERO_LINE_NUMBER = 9
DIVIDE_TO_ZERO_COMMIT_SHA = "fd1aba79fcf9a16b7be72b35e6b53f72d46aaacc"

DIVIDE_TO_ZERO_CALLER_LINE_NUMBER = 13
DIVIDE_TO_ZERO_CALLER_COMMIT_SHA = "38577f25ebb8b2bdc3bf8ec8e3898b6870b9b308"

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
