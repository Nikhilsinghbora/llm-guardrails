from __future__ import annotations

from pathlib import Path

import pytest

from llm_guard.model import Model


def test_from_local_resolves_path(tmp_path):
    model = Model.from_local(tmp_path)
    assert model.path == str(tmp_path.resolve())


def test_from_local_string_path(tmp_path):
    model = Model.from_local(str(tmp_path))
    assert model.path == str(tmp_path.resolve())


def test_from_local_passes_kwargs(tmp_path):
    model = Model.from_local(tmp_path, revision="abc123")
    assert model.revision == "abc123"


def test_from_local_default_fields(tmp_path):
    model = Model.from_local(tmp_path)
    assert model.onnx_path is None
    assert model.subfolder == ""
