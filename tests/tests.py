import os.path
from sys import exc_info

from tests.utils import get_current_tb_extender, TRACEBLAME_GIT_PATH, ALL_FILES_IN_TRACEBLAME_REPO, \
    DIVIDE_TO_ZERO_LINE_NUMBER, divide_by_zero, DIVIDE_TO_ZERO_COMMIT_SHA, DIVIDE_TO_ZERO_CALLER_COMMIT_SHA, \
    DIVIDE_TO_ZERO_CALLER_LINE_NUMBER
from traceblame import iter_stacks


def test_files_in_repo():
    tb_extender = get_current_tb_extender()
    assert sorted(tb_extender.files_in_repo) == sorted(ALL_FILES_IN_TRACEBLAME_REPO)


def test_get_blame_repr():
    tb_extender = get_current_tb_extender()
    divide_to_zero_line_repr = tb_extender.get_blame_repr(
        path=os.path.join(TRACEBLAME_GIT_PATH, "tests", "utils.py"),
        line=DIVIDE_TO_ZERO_LINE_NUMBER,
    )
    assert divide_to_zero_line_repr is not None
    assert divide_to_zero_line_repr.email == "ncopiy@yandex.com", str(divide_to_zero_line_repr)
    assert divide_to_zero_line_repr.commit == DIVIDE_TO_ZERO_COMMIT_SHA

    invalid_line_repr = tb_extender.get_blame_repr(
        path=os.path.join(TRACEBLAME_GIT_PATH, "tests", "ululu", "ulululululululu.py"),
        line=777,
    )
    assert invalid_line_repr is None


def test_get_last_commit():
    tb_extender = get_current_tb_extender()

    commit_of_valid_path = tb_extender.get_last_commit(
        path=os.path.join(TRACEBLAME_GIT_PATH, "tests", "utils.py"),
        line=DIVIDE_TO_ZERO_LINE_NUMBER,
    )
    assert commit_of_valid_path is not None
    assert commit_of_valid_path.author.email == "ncopiy@yandex.com", str(commit_of_valid_path.author)
    assert commit_of_valid_path.hexsha == DIVIDE_TO_ZERO_COMMIT_SHA

    commit_of_invalid_path = tb_extender.get_last_commit(
        path=os.path.join(TRACEBLAME_GIT_PATH, "tests", "ululu", "ulululululululu.py"),
        line=777,
    )
    assert commit_of_invalid_path is None


def test_sys_exc_info_without_blame():
    try:
        divide_by_zero()
    except:  # noqa
        exc_type, exc_value, exc_traceback = exc_info()
        for tb in iter_stacks(exc_traceback):
            assert "blame" not in tb.tb_frame.f_locals


def test_sys_exc_info_with_blame():
    tb_extender = get_current_tb_extender()

    try:
        divide_by_zero()
    except:  # noqa
        exc_type, exc_value, exc_traceback = tb_extender.get_extended_exc_info()
    else:
        assert False, "we expected exception"

    assert exc_type == ZeroDivisionError
    assert exc_value is not None

    any_tb_at_utils = False

    expected_sha_to_line = {
        DIVIDE_TO_ZERO_COMMIT_SHA: DIVIDE_TO_ZERO_LINE_NUMBER,
        DIVIDE_TO_ZERO_CALLER_COMMIT_SHA: DIVIDE_TO_ZERO_CALLER_LINE_NUMBER,
    }

    for tb in iter_stacks(exc_traceback):
        assert "blame" in tb.tb_frame.f_locals

        if "traceblame/tests/utils.py" in tb.tb_frame.f_code.co_filename:
            any_tb_at_utils = True
        else:
            continue

        assert tb.tb_frame.f_locals["blame"].email == "ncopiy@yandex.com", str(tb.tb_frame.f_locals["blame"])
        assert tb.tb_frame.f_locals["blame"].commit in expected_sha_to_line, str(tb.tb_frame.f_locals["blame"])
        assert tb.tb_lineno == expected_sha_to_line[tb.tb_frame.f_locals["blame"].commit], str(tb.tb_frame.f_locals["blame"])

    assert any_tb_at_utils
