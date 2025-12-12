# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from digitalhub_runtime_modelserve.entities.function.kubeaiserve.spec import (
    FunctionSpecKubeaiserve,
    FunctionValidatorKubeaiserve,
)
from digitalhub_runtime_modelserve.entities.function.kubeaiservetext.enums import KubeaiEngine, KubeaiFeature


class FunctionSpecKubeaiserveText(FunctionSpecKubeaiserve):
    """
    FunctionSpecKubeaiserveText specifications.
    """

    def __init__(
        self,
        model_name: str | None = None,
        image: str | None = None,
        url: str | None = None,
        adapters: list[dict] | None = None,
        features: list[dict] | None = None,
        engine: str | None = None,
    ) -> None:
        super().__init__(model_name, image, url, adapters)
        self.features = features
        self.engine = engine


class FunctionValidatorKubeaiserveText(FunctionValidatorKubeaiserve):
    """
    FunctionValidatorKubeaiserveText validator.
    """

    features: Optional[list[KubeaiFeature]] = None
    "Features."

    engine: Optional[KubeaiEngine] = None
    "Engine."
