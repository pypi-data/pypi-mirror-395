# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderKubeaiserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.function.kubeaiserve.entity import FunctionKubeaiserve
from digitalhub_runtime_modelserve.entities.function.kubeaiserve.spec import (
    FunctionSpecKubeaiserve,
    FunctionValidatorKubeaiserve,
)
from digitalhub_runtime_modelserve.entities.function.kubeaiserve.status import FunctionStatusKubeaiserve


class FunctionKubeaiserveBuilder(FunctionBuilder, RuntimeEntityBuilderKubeaiserve):
    """
    FunctionKubeaiserve builder.
    """

    ENTITY_CLASS = FunctionKubeaiserve
    ENTITY_SPEC_CLASS = FunctionSpecKubeaiserve
    ENTITY_SPEC_VALIDATOR = FunctionValidatorKubeaiserve
    ENTITY_STATUS_CLASS = FunctionStatusKubeaiserve
    ENTITY_KIND = EntityKinds.FUNCTION_KUBEAISERVE.value
