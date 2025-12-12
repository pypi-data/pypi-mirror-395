# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderKubeaiserveText
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.run.kubeaiservetext_run.entity import RunKubeaiserveTextRun
from digitalhub_runtime_modelserve.entities.run.kubeaiservetext_run.spec import (
    RunSpecKubeaiserveTextRun,
    RunValidatorKubeaiserveTextRun,
)
from digitalhub_runtime_modelserve.entities.run.kubeaiservetext_run.status import RunStatusKubeaiserveTextRun


class RunKubeaiserveTextRunBuilder(RunBuilder, RuntimeEntityBuilderKubeaiserveText):
    """
    RunKubeaiserveTextRunBuilder runer.
    """

    ENTITY_CLASS = RunKubeaiserveTextRun
    ENTITY_SPEC_CLASS = RunSpecKubeaiserveTextRun
    ENTITY_SPEC_VALIDATOR = RunValidatorKubeaiserveTextRun
    ENTITY_STATUS_CLASS = RunStatusKubeaiserveTextRun
    ENTITY_KIND = EntityKinds.RUN_KUBEAISERVETEXT_SERVE.value
