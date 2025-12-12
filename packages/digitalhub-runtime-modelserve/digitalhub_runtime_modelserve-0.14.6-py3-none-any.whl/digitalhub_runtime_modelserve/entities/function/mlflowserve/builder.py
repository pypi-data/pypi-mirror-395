# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderMlflowserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.function.mlflowserve.entity import FunctionMlflowserve
from digitalhub_runtime_modelserve.entities.function.mlflowserve.spec import (
    FunctionSpecMlflowserve,
    FunctionValidatorMlflowserve,
)
from digitalhub_runtime_modelserve.entities.function.mlflowserve.status import FunctionStatusMlflowserve


class FunctionMlflowserveBuilder(FunctionBuilder, RuntimeEntityBuilderMlflowserve):
    """
    FunctionMlflowserve builder.
    """

    ENTITY_CLASS = FunctionMlflowserve
    ENTITY_SPEC_CLASS = FunctionSpecMlflowserve
    ENTITY_SPEC_VALIDATOR = FunctionValidatorMlflowserve
    ENTITY_STATUS_CLASS = FunctionStatusMlflowserve
    ENTITY_KIND = EntityKinds.FUNCTION_MLFLOWSERVE.value
