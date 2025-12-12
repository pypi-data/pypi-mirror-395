import re
from pathlib import Path
from typing import Union

import structlog

from libfelix.regex import single_match_from_file

log = structlog.get_logger()


class GitError(Exception):
    pass


class NoRepoError(GitError):
    pass


class NoHeadError(GitError):
    pass


class Repo:
    """
    Get info from a git repo.
    This avoids big dependencies like pygit2 and libgit.
    """

    RE_REF = re.compile(r'^ref: (.+)$')

    def __init__(self, path: Union[Path, str] = '.'):
        self.path = Path(path)
        self.dotgit = self.path / '.git'
        log.debug('check for git dir', path=self.dotgit)
        if not self.dotgit.is_dir():
            raise NoRepoError(f'Not a repo: {self.path}')
        self._head_file = self.dotgit / 'HEAD'

    @property
    def head(self):
        path = single_match_from_file(self.RE_REF, self._head_file)
        log.debug('read head file', source=self._head_file, path=path)
        try:
            return self.dotgit.joinpath(path).read_text().strip()
        except FileNotFoundError:
            raise NoHeadError('no HEAD revision (NOBRANCH)')
