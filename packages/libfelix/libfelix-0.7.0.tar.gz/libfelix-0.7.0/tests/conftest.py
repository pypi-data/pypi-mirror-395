import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def path_repo_empty(tmpdir) -> Path:
    subprocess.check_call('git init empty', shell=True, cwd=tmpdir)
    return tmpdir / 'empty'


@pytest.fixture
def path_repo(tmpdir) -> Path:
    path = tmpdir / 'test'
    subprocess.check_call('git init test', shell=True, cwd=tmpdir)
    subprocess.check_call(
        'git commit --allow-empty -m "foo"', shell=True, cwd=path
    )
    return path
