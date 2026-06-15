from __future__ import annotations

import pytest

from llm_guard.mixins import ThresholdMixin
from llm_guard.util import validate_threshold


class _FakeScanner(ThresholdMixin):
    """Minimal scanner that uses ThresholdMixin without a real model."""

    def __init__(self, threshold: float = 0.5) -> None:
        validate_threshold(threshold)
        self._threshold = threshold

    def scan(self, prompt: str) -> tuple[str, bool, float]:
        # Trivial scan: flag if prompt length exceeds threshold*100
        if len(prompt) > self._threshold * 100:
            return prompt, False, 1.0
        return prompt, True, -1.0


# ── getter ─────────────────────────────────────────────────────────────────────


def test_threshold_getter_returns_init_value():
    assert _FakeScanner(threshold=0.7).threshold == 0.7


def test_threshold_getter_low():
    assert _FakeScanner(threshold=0.0).threshold == 0.0


def test_threshold_getter_high():
    assert _FakeScanner(threshold=1.0).threshold == 1.0


# ── setter – valid values ───────────────────────────────────────────────────────


@pytest.mark.parametrize("new_val", [0.0, 0.1, 0.5, 0.75, 0.99, 1.0])
def test_threshold_setter_valid(new_val):
    s = _FakeScanner(threshold=0.5)
    s.threshold = new_val
    assert s.threshold == new_val


def test_threshold_setter_repeated_updates():
    s = _FakeScanner(threshold=0.5)
    for val in [0.1, 0.9, 0.3, 1.0, 0.0]:
        s.threshold = val
        assert s.threshold == val


def test_threshold_setter_same_value_idempotent():
    s = _FakeScanner(threshold=0.6)
    s.threshold = 0.6
    assert s.threshold == 0.6


# ── setter – invalid values ─────────────────────────────────────────────────────


@pytest.mark.parametrize("bad_val", [1.0001, 1.1, 2.0, 100.0])
def test_threshold_setter_above_one_raises(bad_val):
    s = _FakeScanner()
    with pytest.raises(ValueError):
        s.threshold = bad_val


@pytest.mark.parametrize("bad_val", [-0.0001, -0.1, -1.0, -100.0])
def test_threshold_setter_below_zero_raises(bad_val):
    s = _FakeScanner()
    with pytest.raises(ValueError):
        s.threshold = bad_val


def test_threshold_setter_nan_raises():
    s = _FakeScanner()
    with pytest.raises((ValueError, Exception)):
        s.threshold = float("nan")


# ── behavioural: scan respects the updated threshold ───────────────────────────


def test_scan_changes_after_threshold_update():
    """Raising threshold makes the scanner less strict."""
    s = _FakeScanner(threshold=0.2)  # flags prompts >20 chars
    long_prompt = "a" * 25

    _, valid_strict, _ = s.scan(long_prompt)
    assert valid_strict is False  # caught at threshold 0.2

    s.threshold = 0.9  # now flags >90 chars
    _, valid_lenient, _ = s.scan(long_prompt)
    assert valid_lenient is True  # not caught at threshold 0.9


def test_scan_catches_more_after_lowering_threshold():
    """Lowering threshold makes the scanner more strict."""
    s = _FakeScanner(threshold=0.9)  # flags prompts >90 chars
    medium_prompt = "a" * 50

    _, valid_lenient, _ = s.scan(medium_prompt)
    assert valid_lenient is True

    s.threshold = 0.3  # now flags >30 chars
    _, valid_strict, _ = s.scan(medium_prompt)
    assert valid_strict is False


# ── multiple instances are independent ─────────────────────────────────────────


def test_instances_have_independent_thresholds():
    s1 = _FakeScanner(threshold=0.2)
    s2 = _FakeScanner(threshold=0.8)
    s1.threshold = 0.9
    assert s2.threshold == 0.8  # s2 unaffected
