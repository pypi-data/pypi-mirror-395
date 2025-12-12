from datetime import datetime

from aecg.utils import parse_hl7_timestamps


def test_different_length_timestamps():
    assert parse_hl7_timestamps("2004") == datetime(year=2004, month=1, day=1)
    assert parse_hl7_timestamps("200410") == datetime(year=2004, month=10, day=1)
    assert parse_hl7_timestamps("20041004") == datetime(year=2004, month=10, day=4)
    assert parse_hl7_timestamps("2004100415") == datetime(
        year=2004, month=10, day=4, hour=15
    )
    assert parse_hl7_timestamps("200410041545") == datetime(
        year=2004, month=10, day=4, hour=15, minute=45
    )
    assert parse_hl7_timestamps("20041004154508") == datetime(
        year=2004, month=10, day=4, hour=15, minute=45, second=8
    )
    assert parse_hl7_timestamps("20041004154508.034") == datetime(
        year=2004, month=10, day=4, hour=15, minute=45, second=8, microsecond=34000
    )
