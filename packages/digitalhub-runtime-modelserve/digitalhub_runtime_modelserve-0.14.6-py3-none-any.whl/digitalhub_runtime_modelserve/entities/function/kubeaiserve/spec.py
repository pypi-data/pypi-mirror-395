# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from digitalhub.entities.function._base.spec import FunctionSpec, FunctionValidator
from pydantic import Field

from digitalhub_runtime_modelserve.entities.function.kubeaiserve.models import KubeaiAdapter

regexp = (
    r"^(store://([^/]+)/model/huggingface/.*)"
    + r"|"
    + r"^pvc?://.*$"
    + r"|"
    + r"^s3?://.*$"
    + r"|"
    + r"^ollama?://.*$"
    + r"|"
    + r"^hf?://.*$"
)


class FunctionSpecKubeaiserve(FunctionSpec):
    """
    FunctionSpecKubeaiserve specifications.
    """

    def __init__(
        self,
        model_name: str | None = None,
        image: str | None = None,
        url: str | None = None,
        adapters: list[dict] | None = None,
        engine: str | None = None,
    ) -> None:
        super().__init__()
        self.model_name = model_name
        self.image = image
        self.url = url
        self.adapters = adapters
        self.engine = engine


class FunctionValidatorKubeaiserve(FunctionValidator):
    """
    FunctionValidatorKubeaiserve validator.
    """

    model_name: Optional[str] = None
    "Model name."

    image: Optional[str] = None
    "Image where the function will be executed."

    url: Optional[str] = Field(pattern=regexp, default=None)
    "Model URL."

    adapters: Optional[list[KubeaiAdapter]] = None
    "Adapters."
