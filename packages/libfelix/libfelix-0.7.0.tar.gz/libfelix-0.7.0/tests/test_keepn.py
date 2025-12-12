import time

import pytest

from libfelix.filesystem import keepn


@pytest.fixture
def dump_dir(tmp_path):
    for i in range(1, 45 + 1):
        filename = f'{i:02}.dump'
        tmp_path.joinpath(filename).touch()
        time.sleep(0.01)  # to get different modified times (mtime)
    return tmp_path


def test_e2e(dump_dir):
    assert len(list(dump_dir.glob('*'))) == 45

    keepn(dump_dir, n_keep=40)
    files = list(dump_dir.glob('*'))
    assert len(files) == 40
    # first few get removed
    assert '01.dump' not in str(files)
    assert '05.dump' not in str(files)
    # rest stays
    assert '06.dump' in str(files)
    assert '45.dump' in str(files)
