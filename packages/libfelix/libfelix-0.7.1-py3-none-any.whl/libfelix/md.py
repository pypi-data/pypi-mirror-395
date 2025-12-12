from pathlib import Path
from typing import Iterator


def iter_md_files(root_dir: Path = Path('.')) -> Iterator[Path]:
    yield from root_dir.rglob('*.md')
