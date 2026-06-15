from __future__ import annotations

import dataclasses
from pathlib import Path

from .util import device


@dataclasses.dataclass
class Model:
    """
    Dataclass to store model information.

    Attributes:
        path (str): Path to the model.
        subfolder (str): Subfolder in the model path.
        revision (str, optional): Revision of the model.
        onnx_path (str, optional): Path to the ONNX model.
        onnx_revision (str, optional): Revision of the ONNX model.
        onnx_subfolder (str): Subfolder in the ONNX model path.
        kwargs (Dict, optional): Keyword arguments passed to the model (transformers).
        pipeline_kwargs (Dict, optional): Keyword arguments passed to the pipeline (transformers).
    """

    path: str
    subfolder: str = ""
    revision: str | None = None
    onnx_path: str | None = None
    onnx_revision: str | None = None
    onnx_subfolder: str = ""
    onnx_filename: str = "model.onnx"
    kwargs: dict = dataclasses.field(default_factory=dict)
    pipeline_kwargs: dict = dataclasses.field(default_factory=dict)
    tokenizer_kwargs: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        default_pipeline_kwargs = {
            "batch_size": 1,
            "device": device(),
        }
        self.pipeline_kwargs = {**default_pipeline_kwargs, **self.pipeline_kwargs}

    @classmethod
    def from_local(cls, path: str | Path, **kwargs) -> Model:
        """
        Create a Model from a local directory.

        Resolves the path to an absolute string so HuggingFace
        ``from_pretrained`` can locate it without ambiguity.

        Example::

            model = Model.from_local("/models/my-deberta")
            scanner = PromptInjection(model=model)
        """
        resolved = str(Path(path).resolve())
        return cls(path=resolved, **kwargs)

    def __str__(self):
        return self.path
