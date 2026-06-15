from __future__ import annotations

from pathlib import Path

import pytest

from llm_guard.model import Model


# ── from_local: path resolution ────────────────────────────────────────────────

def test_from_local_path_object(tmp_path):
    model = Model.from_local(tmp_path)
    assert model.path == str(tmp_path.resolve())


def test_from_local_string_path(tmp_path):
    model = Model.from_local(str(tmp_path))
    assert model.path == str(tmp_path.resolve())


def test_from_local_returns_absolute_path(tmp_path):
    model = Model.from_local(tmp_path)
    assert Path(model.path).is_absolute()


def test_from_local_nested_dir(tmp_path):
    nested = tmp_path / "models" / "v1"
    nested.mkdir(parents=True)
    model = Model.from_local(nested)
    assert model.path == str(nested.resolve())


def test_from_local_passes_revision(tmp_path):
    model = Model.from_local(tmp_path, revision="abc123")
    assert model.revision == "abc123"


def test_from_local_passes_onnx_path(tmp_path):
    model = Model.from_local(tmp_path, onnx_path="org/model-onnx")
    assert model.onnx_path == "org/model-onnx"


def test_from_local_passes_subfolder(tmp_path):
    model = Model.from_local(tmp_path, subfolder="onnx")
    assert model.subfolder == "onnx"


# ── from_local: default field values ───────────────────────────────────────────

def test_from_local_default_onnx_path_is_none(tmp_path):
    model = Model.from_local(tmp_path)
    assert model.onnx_path is None


def test_from_local_default_revision_is_none(tmp_path):
    model = Model.from_local(tmp_path)
    assert model.revision is None


def test_from_local_default_subfolder_is_empty(tmp_path):
    model = Model.from_local(tmp_path)
    assert model.subfolder == ""


# ── __post_init__: default pipeline_kwargs are injected ────────────────────────

def test_model_pipeline_kwargs_gets_batch_size(tmp_path):
    model = Model.from_local(tmp_path, pipeline_kwargs={"max_length": 512})
    assert model.pipeline_kwargs["batch_size"] == 1


def test_model_pipeline_kwargs_gets_device(tmp_path):
    model = Model.from_local(tmp_path)
    assert "device" in model.pipeline_kwargs


def test_model_explicit_pipeline_kwargs_override_defaults(tmp_path):
    model = Model.from_local(tmp_path, pipeline_kwargs={"batch_size": 4})
    assert model.pipeline_kwargs["batch_size"] == 4


def test_model_user_pipeline_kwargs_merged_with_defaults(tmp_path):
    model = Model.from_local(tmp_path, pipeline_kwargs={"top_k": None, "max_length": 128})
    assert model.pipeline_kwargs["top_k"] is None
    assert model.pipeline_kwargs["max_length"] == 128
    assert "batch_size" in model.pipeline_kwargs


# ── str representation ─────────────────────────────────────────────────────────

def test_model_str_returns_path(tmp_path):
    model = Model.from_local(tmp_path)
    assert str(model) == str(tmp_path.resolve())


# ── from_local is equivalent to direct construction ────────────────────────────

def test_from_local_equivalent_to_direct_construction(tmp_path):
    resolved = str(tmp_path.resolve())
    via_factory = Model.from_local(tmp_path, revision="r1")
    via_direct = Model(path=resolved, revision="r1")
    assert via_factory.path == via_direct.path
    assert via_factory.revision == via_direct.revision
