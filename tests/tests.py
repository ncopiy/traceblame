import os.path
from sys import exc_info

from tests.utils import get_current_tb_extender, TRACEBLAME_GIT_PATH
from traceblame import iter_stacks


def test_files_in_repo():
    expected = {
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
    tb_extender = get_current_tb_extender()
    assert sorted(tb_extender.files_in_repo) == sorted(expected)


def divide():
    return 10 / 0


def test_get_blame_repr():
    tb_extender = get_current_tb_extender()
    divide_to_zero_line_repr = tb_extender.get_blame_repr(
        path=os.path.join(TRACEBLAME_GIT_PATH, "tests", "tests.py"),
        line=29,
    )
    assert divide_to_zero_line_repr is not None
    assert divide_to_zero_line_repr.email == "ncopiy@ya.ru", str(divide_to_zero_line_repr)
    assert divide_to_zero_line_repr.commit == "99b7c490fc0344b0f31a931f6c6f4c3b89c2da9e"


def test_sys_exc_info_without_blame():
    try:
        divide()
    except:  # noqa
        exc_type, exc_value, exc_traceback = exc_info()
        for tb in iter_stacks(exc_traceback):
            assert "blame" not in tb.tb_frame.f_locals


def test_sys_exc_info_with_blame():
    tb_extender = get_current_tb_extender()

    try:
        divide()
    except:  # noqa
        exc_type, exc_value, exc_traceback = tb_extender.get_extended_exc_info()
        assert exc_type == ZeroDivisionError
        assert exc_value is not None
        for tb in iter_stacks(exc_traceback):
            assert "blame" in tb.tb_frame.f_locals

            # ref https://github.com/ncopiy/traceblame/commit/99b7c490fc0344b0f31a931f6c6f4c3b89c2da9e
            assert "traceblame/tests/tests.py" in tb.tb_frame.f_code.co_filename
            line = tb.tb_lineno
            assert line in [
                56,  # line number of `divide()` code in this function in `try` block
                29,  # line number of `return 10 / 0` code in this file
            ], line

            assert tb.tb_frame.f_locals["blame"].email == "ncopiy@ya.ru", str(tb.tb_frame.f_locals["blame"])
            assert tb.tb_frame.f_locals["blame"].commit == "99b7c490fc0344b0f31a931f6c6f4c3b89c2da9e"
