# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderMlflowserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.run.mlflowserve_build_run.entity import RunMlflowserveBuildRun
from digitalhub_runtime_modelserve.entities.run.mlflowserve_build_run.spec import (
    RunSpecMlflowserveBuildRun,
    RunValidatorMlflowserveBuildRun,
)
from digitalhub_runtime_modelserve.entities.run.mlflowserve_build_run.status import RunStatusMlflowserveBuildRun


class RunMlflowserveBuildRunBuilder(RunBuilder, RuntimeEntityBuilderMlflowserve):
    """
    RunMlflowserveBuildRunBuilder runer.
    """

    ENTITY_CLASS = RunMlflowserveBuildRun
    ENTITY_SPEC_CLASS = RunSpecMlflowserveBuildRun
    ENTITY_SPEC_VALIDATOR = RunValidatorMlflowserveBuildRun
    ENTITY_STATUS_CLASS = RunStatusMlflowserveBuildRun
    ENTITY_KIND = EntityKinds.RUN_MLFLOWSERVE_BUILD.value
