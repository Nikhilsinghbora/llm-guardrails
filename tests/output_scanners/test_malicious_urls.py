from __future__ import annotations

import pytest

from llm_guard.output_scanners.malicious_urls import MaliciousURLs

# ── full integration tests (uses real model) ───────────────────────────────────


@pytest.mark.parametrize(
    "output,expected_valid,expected_score",
    [
        (
            "It's https://google.com/.",
            True,
            -0.5,
        ),
        (
            "It's http://socialsocietyedu.com/components/com_wa/config.bin and http://facebuk.co/signup.html",
            False,
            0.5,
        ),
        (
            "It's https://google.com/ and https://facebook.com/.",
            True,
            -0.6,
        ),
    ],
)
def test_scan(output, expected_valid, expected_score):
    scanner = MaliciousURLs()
    sanitized_output, valid, score = scanner.scan("", output)
    assert sanitized_output == output
    assert valid == expected_valid
    assert score == expected_score


def test_empty_output_is_valid():
    scanner = MaliciousURLs()
    _, valid, score = scanner.scan("", "")
    assert valid is True
    assert score == -1.0


def test_output_with_no_urls_is_valid():
    scanner = MaliciousURLs()
    _, valid, score = scanner.scan("", "There are no links in this response.")
    assert valid is True
    assert score == -1.0


def test_output_with_whitespace_only_is_valid():
    scanner = MaliciousURLs()
    _, valid, score = scanner.scan("", "   \n  ")
    assert valid is True
    assert score == -1.0


# ── fix #318: top_k auto-injection (unit, no model load) ─────────────────────


def test_top_k_injected_when_absent_from_pipeline_kwargs(monkeypatch):
    """When a custom model omits top_k, MaliciousURLs must inject top_k=None
    so the pipeline returns list-of-dicts instead of a plain string."""
    from llm_guard.model import Model

    captured = {}

    def mock_pipeline(task, model, tokenizer, **kwargs):
        captured.update(kwargs)
        return lambda urls: [[{"label": "benign", "score": 0.99}] for _ in urls]

    def mock_get_tok_model(model, use_onnx):
        return object(), object()

    monkeypatch.setattr("llm_guard.output_scanners.malicious_urls.pipeline", mock_pipeline)
    monkeypatch.setattr(
        "llm_guard.output_scanners.malicious_urls.get_tokenizer_and_model_for_classification",
        mock_get_tok_model,
    )

    model_without_top_k = Model(path="test/model", pipeline_kwargs={"max_length": 128})
    assert "top_k" not in model_without_top_k.pipeline_kwargs

    MaliciousURLs(model=model_without_top_k)
    assert captured.get("top_k") is None, "top_k=None was not injected"


def test_top_k_explicit_value_is_not_overridden(monkeypatch):
    """An explicit top_k value in pipeline_kwargs must not be replaced."""
    from llm_guard.model import Model

    captured = {}

    def mock_pipeline(task, model, tokenizer, **kwargs):
        captured.update(kwargs)
        return lambda urls: [[{"label": "benign", "score": 0.99}] for _ in urls]

    def mock_get_tok_model(model, use_onnx):
        return object(), object()

    monkeypatch.setattr("llm_guard.output_scanners.malicious_urls.pipeline", mock_pipeline)
    monkeypatch.setattr(
        "llm_guard.output_scanners.malicious_urls.get_tokenizer_and_model_for_classification",
        mock_get_tok_model,
    )

    model_with_top_k = Model(path="test/model", pipeline_kwargs={"max_length": 128, "top_k": 3})
    MaliciousURLs(model=model_with_top_k)
    assert captured.get("top_k") == 3, "Explicit top_k was overridden unexpectedly"
