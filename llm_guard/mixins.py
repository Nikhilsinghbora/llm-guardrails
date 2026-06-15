from __future__ import annotations

from llm_guard.util import validate_threshold


class ThresholdMixin:
    """
    Mixin that exposes `threshold` as a readable and writable property.

    Apply to any scanner that stores its detection threshold as `_threshold`
    so callers can adjust sensitivity without reinitialising the scanner
    (and reloading its model).

    Example::

        scanner = PromptInjection(threshold=0.92)
        scanner.threshold = 0.80   # lower bar, more sensitive
    """

    _threshold: float

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, value: float) -> None:
        validate_threshold(value)
        self._threshold = value
