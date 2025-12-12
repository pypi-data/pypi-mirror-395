import pytest

from libfelix.git import Repo, NoRepoError, NoHeadError


def test(path_repo):
    r = Repo(path_repo)
    assert len(r.head) == 40


def test_no_repo(tmpdir):
    with pytest.raises(NoRepoError):
        Repo(tmpdir)


def test_head_empty(path_repo_empty):
    r = Repo(path_repo_empty)
    with pytest.raises(NoHeadError):
        r.head
    # assert len(r.rev) == 40
