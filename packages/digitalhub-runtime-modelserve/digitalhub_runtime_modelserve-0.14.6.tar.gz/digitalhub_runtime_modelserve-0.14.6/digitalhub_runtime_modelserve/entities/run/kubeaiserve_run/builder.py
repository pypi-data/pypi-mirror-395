# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderKubeaiserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.entity import RunKubeaiserveRun
from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.spec import (
    RunSpecKubeaiserveRun,
    RunValidatorKubeaiserveRun,
)
from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.status import RunStatusKubeaiserveRun


class RunKubeaiserveRunBuilder(RunBuilder, RuntimeEntityBuilderKubeaiserve):
    """
    RunKubeaiserveRunBuilder runer.
    """

    ENTITY_CLASS = RunKubeaiserveRun
    ENTITY_SPEC_CLASS = RunSpecKubeaiserveRun
    ENTITY_SPEC_VALIDATOR = RunValidatorKubeaiserveRun
    ENTITY_STATUS_CLASS = RunStatusKubeaiserveRun
    ENTITY_KIND = EntityKinds.RUN_KUBEAISERVE_SERVE.value
