from trace_blame import ExtendedRepo, get_exc_info_with_blame_func, iter_stacks


def test_files_in_repo():
    expected = {
        '.github/workflows/pep8.yml',
        '.gitignore',
        'trace_blame/main.py',
        'trace_blame/__init__.py',
        'requirements.txt',
        'tests.py',
    }
    repo = ExtendedRepo()
    assert sorted(repo.files_in_repo) == sorted(expected)


def divide():
    return 10 / 0


def test_sys_exc_info_without_blame():
    from sys import exc_info

    try:
        divide()
    except:  # noqa
        exc_type, exc_value, exc_traceback = exc_info()
        for tb in iter_stacks(exc_traceback):
            assert "blame" not in tb.tb_frame.f_locals


def test_sys_exc_info_with_blame():
    import os

    exc_info_func = get_exc_info_with_blame_func(os.path.dirname(os.path.abspath(__file__)))

    try:
        divide()
    except:  # noqa
        exc_type, exc_value, exc_traceback = exc_info_func()
        assert exc_type == ZeroDivisionError
        assert exc_value is not None
        for tb in iter_stacks(exc_traceback):
            assert "blame" in tb.tb_frame.f_locals
