from __future__ import annotations

import pytest

from llm_guard.exception import LLMGuardValidationError
from llm_guard.mixins import ThresholdMixin


class _FakeScanner(ThresholdMixin):
    def __init__(self, threshold: float = 0.5) -> None:
        from llm_guard.util import validate_threshold

        validate_threshold(threshold)
        self._threshold = threshold

    def scan(self, prompt: str):
        return prompt, True, -1.0


def test_threshold_getter():
    s = _FakeScanner(threshold=0.7)
    assert s.threshold == 0.7


def test_threshold_setter_valid():
    s = _FakeScanner(threshold=0.5)
    s.threshold = 0.9
    assert s.threshold == 0.9


def test_threshold_setter_zero():
    s = _FakeScanner()
    s.threshold = 0.0
    assert s.threshold == 0.0


def test_threshold_setter_one():
    s = _FakeScanner()
    s.threshold = 1.0
    assert s.threshold == 1.0


def test_threshold_setter_invalid_above_one():
    s = _FakeScanner()
    with pytest.raises(LLMGuardValidationError):
        s.threshold = 1.1


def test_threshold_setter_invalid_negative():
    s = _FakeScanner()
    with pytest.raises(LLMGuardValidationError):
        s.threshold = -0.1
