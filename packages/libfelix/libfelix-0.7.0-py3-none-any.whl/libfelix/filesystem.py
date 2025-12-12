from os.path import getmtime
from pathlib import Path
from typing import Iterable

import structlog

log = structlog.get_logger()


def by_date_desc(paths: Iterable[Path]) -> list:
    return list(reversed(sorted(paths, key=getmtime)))


def keepn(directory: Path, n_keep: int, dryrun=False):
    paths = by_date_desc(directory.iterdir())
    keep, delete = paths[:n_keep], paths[n_keep:]
    log.info('keep', paths=[str(x) for x in sorted(keep, key=getmtime)])
    log.info('delete', paths=[str(x) for x in sorted(delete, key=getmtime)])
    if dryrun:
        log.info('DRYRUN. returning.')
        return
    else:
        for path in delete:
            path.unlink()
