# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import (
    RuntimeEntityBuilderKubeaiserveSpeechtotext,
)
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.run.kubeaiservespeechtotext_run.entity import RunKubeaiserveSpeechtotextRun
from digitalhub_runtime_modelserve.entities.run.kubeaiservespeechtotext_run.spec import (
    RunSpecKubeaiserveSpeechtotextRun,
    RunValidatorKubeaiserveSpeechtotextRun,
)
from digitalhub_runtime_modelserve.entities.run.kubeaiservespeechtotext_run.status import (
    RunStatusKubeaiserveSpeechtotextRun,
)


class RunKubeaiserveSpeechtotextRunBuilder(RunBuilder, RuntimeEntityBuilderKubeaiserveSpeechtotext):
    """
    RunKubeaiserveSpeechtotextRunBuilder runer.
    """

    ENTITY_CLASS = RunKubeaiserveSpeechtotextRun
    ENTITY_SPEC_CLASS = RunSpecKubeaiserveSpeechtotextRun
    ENTITY_SPEC_VALIDATOR = RunValidatorKubeaiserveSpeechtotextRun
    ENTITY_STATUS_CLASS = RunStatusKubeaiserveSpeechtotextRun
    ENTITY_KIND = EntityKinds.RUN_KUBEAISERVESPEECHTOTEXT_SERVE.value
