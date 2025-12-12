from pathlib import Path

import pytest
from _pytest.pathlib import make_numbered_dir_with_cleanup
from filelock import FileLock


def rm_tree(pth):
    for child in pth.glob("*"):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def pytest_addoption(parser):
    parser.addoption("--cached-tmpdir", action="store", default=None)


@pytest.fixture(scope="session")
def cached_tmpdir(tmp_path_factory, pytestconfig):
    """
    This fixture provides a way to override a temp directory from the cli so
    that it can be reused between test runs.
    """
    cached_dir = pytestconfig.getoption("--cached-tmpdir")
    if not cached_dir:
        # Setup a temp dir which is shared between all workers
        root_tmp_dir = tmp_path_factory.getbasetemp().parent
        # Directly using this internal function of pytest is probably a bad
        # idea, however, I don't know how we can get a temp dir which isn't
        # unique to the process and gets automatically cleaned up otherwise.
        yield make_numbered_dir_with_cleanup(
            root=root_tmp_dir, prefix="dkist-inventory", keep=False, lock_timeout=60, mode=0o700
        )

    else:
        cached_dir = Path(cached_dir).expanduser().absolute()
        if not cached_dir.exists():
            cached_dir.mkdir()

        yield cached_dir
