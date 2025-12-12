import re
from pathlib import Path


class NoMatchException(Exception):
    pass


def single_match_from_file(regex: re.Pattern, path: Path):
    with path.open('r') as f:
        m = re.match(r'^ref: (.+)$', f.read())
    if m is None:
        raise NoMatchException(f'No match for {regex} in {path}')
    return m.group(1)
