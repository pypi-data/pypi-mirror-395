# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderMlflowserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.run.mlflowserve_serve_run.entity import RunMlflowserveServeRun
from digitalhub_runtime_modelserve.entities.run.mlflowserve_serve_run.spec import (
    RunSpecMlflowserveServeRun,
    RunValidatorMlflowserveServeRun,
)
from digitalhub_runtime_modelserve.entities.run.mlflowserve_serve_run.status import RunStatusMlflowserveServeRun


class RunMlflowserveServeRunBuilder(RunBuilder, RuntimeEntityBuilderMlflowserve):
    """
    RunMlflowserveServeRunBuilder runer.
    """

    ENTITY_CLASS = RunMlflowserveServeRun
    ENTITY_SPEC_CLASS = RunSpecMlflowserveServeRun
    ENTITY_SPEC_VALIDATOR = RunValidatorMlflowserveServeRun
    ENTITY_STATUS_CLASS = RunStatusMlflowserveServeRun
    ENTITY_KIND = EntityKinds.RUN_MLFLOWSERVE_SERVE.value
