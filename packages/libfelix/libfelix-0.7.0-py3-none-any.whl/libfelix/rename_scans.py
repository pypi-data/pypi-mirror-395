from dateutil import parser
from pathlib import Path
import re
import shutil
import sys
import uuid
import fnmatch

import inotify.adapters

import structlog

from libfelix.logging import configure_structlog_console_from_env

log = structlog.get_logger()


class MickeysoftGerman(parser.parserinfo):
    # I am sure about Sept and Dez ;)
    MONTHS = [
        ('Jan', 'Jan'),
        ('Feb', 'Feb'),
        ('Mär', 'Mar'),
        ('Apr', 'Apr'),
        ('Mai', 'May'),
        ('Jun', 'Jun'),
        ('Jul', 'Jul'),
        ('Aug', 'Aug'),
        ('Sept', 'Sep'),
        ('Okt', 'Oct'),
        ('Nov', 'Nov'),
        ('Dez', 'Dec'),
    ]


def parse_date_str(date_str: str):
    # trailing dot in `Scan 16 Sept. 25 20·36·09.pdf`
    date_str = date_str.replace('.', '')
    result = parser.parse(date_str, parserinfo=MickeysoftGerman())
    return result


def handle_path(path) -> Path | None:
    if not path.exists() or not path.name.lower().endswith('.pdf'):
        log.debug('File does not exist or is not a PDF, exiting')
        return

    filename = path.name

    date_match = re.search(r'\d{2} [\w.]+ \d{2}', filename)

    if not date_match:
        log.debug('Could not find date pattern in filename', filename=filename)
        return

    date_str = date_match.group(0)
    dt_obj = parse_date_str(date_str)
    formatted_date = dt_obj.strftime('%Y-%m-%d')

    target_filename = f'{formatted_date}.pdf'
    target_path = path.parent / target_filename

    if target_path.exists():
        stem = target_path.stem
        suffix = target_path.suffix
        uuid_str = str(uuid.uuid4())
        target_filename = f'{stem}-{uuid_str}{suffix}'
        target_path = path.parent / target_filename

    shutil.move(path, target_path)
    log.info('moved scan', source=str(path), target=str(target_path))
    return target_path


def main():
    configure_structlog_console_from_env()
    scan_dir = Path(sys.argv[1])
    log.info('Running on all files found', scan_dir=str(scan_dir))
    for file_path in scan_dir.glob('Scan*.pdf'):
        log.debug('Detected matching file', file_path=str(file_path))
        handle_path(file_path)

    log.info('Starting inotify watch', scan_dir=str(scan_dir))

    i = inotify.adapters.InotifyTree(str(scan_dir))

    try:
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event

            # Only process file creation/move events
            if 'IN_CLOSE_WRITE' in type_names or 'IN_MOVED_TO' in type_names:
                if filename and fnmatch.fnmatch(filename, 'Scan*.pdf'):
                    file_path = Path(path) / filename
                    log.debug(
                        'Detected matching file', file_path=str(file_path)
                    )
                    handle_path(file_path)
    except KeyboardInterrupt:
        log.info('Stopping inotify watch')


if __name__ == '__main__':
    main()
