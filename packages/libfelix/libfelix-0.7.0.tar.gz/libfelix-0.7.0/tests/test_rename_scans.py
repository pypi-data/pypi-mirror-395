import datetime
from libfelix.rename_scans import parse_date_str


def test_parse_date_str():
    assert parse_date_str('16 Sept. 25') == datetime.datetime(2025, 9, 16)
    assert parse_date_str('01 Dez. 25') == datetime.datetime(2025, 12, 1)
