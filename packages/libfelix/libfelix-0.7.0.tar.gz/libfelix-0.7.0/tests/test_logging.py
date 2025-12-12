from libfelix.logging import configure_structlog_console, get_logger


def test(capsys):
    configure_structlog_console('INFO')

    log = get_logger()
    log.info('hi')
    captured = capsys.readouterr()
    assert 'info' in captured.err
    assert 'hi' in captured.err

    log.error('fail')
    captured = capsys.readouterr()
    assert 'error' in captured.err
    assert 'fail' in captured.err
