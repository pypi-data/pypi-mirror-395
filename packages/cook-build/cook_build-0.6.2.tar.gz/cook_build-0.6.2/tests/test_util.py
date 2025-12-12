from cook import util
from datetime import datetime, timedelta
import hashlib
from pathlib import Path


def test_evaluate_digest(tmp_wd: Path) -> None:
    fn = tmp_wd / "foo.txt"
    fn.write_text("bar")
    assert util.evaluate_hexdigest(fn) == hashlib.sha1(b"bar").hexdigest()


def test_format_timedelta() -> None:
    assert (
        util.format_timedelta(timedelta(1, 13, 17, 28, 40, 3, 8)) == "57 days, 3:40:13"
    )
    assert util.format_timedelta(timedelta(microseconds=999)) == "0:00:00.000999"


def test_format_datetime() -> None:
    assert (
        util.format_datetime(datetime(2023, 7, 25, 13, 7, 9, 777))
        == "2023-07-25 13:07:09"
    )
