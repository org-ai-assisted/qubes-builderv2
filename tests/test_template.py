import time

from qubesbuilder.plugins.template import (
    source_date_epoch_from_template_timestamp,
)


def test_source_date_epoch_from_template_timestamp():
    # TEMPLATE_TIMESTAMP ("%Y%m%d%H%M") is UTC; the epoch must match `date -u`.
    assert (
        source_date_epoch_from_template_timestamp("202511280430")
        == "1764304200"
    )
    assert source_date_epoch_from_template_timestamp("197001010000") == "0"


def test_source_date_epoch_timezone_stable(monkeypatch):
    # The timestamp is UTC, so a non-UTC local TZ must not shift the epoch
    # (regresses a naive-datetime derivation that would read it as local time).
    monkeypatch.setenv("TZ", "America/New_York")
    time.tzset()
    try:
        assert (
            source_date_epoch_from_template_timestamp("202511280430")
            == "1764304200"
        )
    finally:
        monkeypatch.delenv("TZ", raising=False)
        time.tzset()
