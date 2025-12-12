# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderKubeaiserveText
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.function.kubeaiservetext.entity import FunctionKubeaiserveText
from digitalhub_runtime_modelserve.entities.function.kubeaiservetext.spec import (
    FunctionSpecKubeaiserveText,
    FunctionValidatorKubeaiserveText,
)
from digitalhub_runtime_modelserve.entities.function.kubeaiservetext.status import FunctionStatusKubeaiserveText


class FunctionKubeaiserveTextBuilder(FunctionBuilder, RuntimeEntityBuilderKubeaiserveText):
    """
    FunctionKubeaiserveText builder.
    """

    ENTITY_CLASS = FunctionKubeaiserveText
    ENTITY_SPEC_CLASS = FunctionSpecKubeaiserveText
    ENTITY_SPEC_VALIDATOR = FunctionValidatorKubeaiserveText
    ENTITY_STATUS_CLASS = FunctionStatusKubeaiserveText
    ENTITY_KIND = EntityKinds.FUNCTION_KUBEAISERVETEXT.value
