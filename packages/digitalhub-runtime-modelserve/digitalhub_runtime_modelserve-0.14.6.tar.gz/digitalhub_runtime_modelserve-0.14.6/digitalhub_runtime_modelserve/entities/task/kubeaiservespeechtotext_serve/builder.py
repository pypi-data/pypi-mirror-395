# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import (
    RuntimeEntityBuilderKubeaiserveSpeechtotext,
)
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.task.kubeaiservespeechtotext_serve.entity import (
    TaskKubeaiserveSpeechtotextServe,
)
from digitalhub_runtime_modelserve.entities.task.kubeaiservespeechtotext_serve.spec import (
    TaskSpecKubeaiserveSpeechtotextServe,
    TaskValidatorKubeaiserveSpeechtotextServe,
)
from digitalhub_runtime_modelserve.entities.task.kubeaiservespeechtotext_serve.status import (
    TaskStatusKubeaiserveSpeechtotextServe,
)


class TaskKubeaiserveSpeechtotextServeBuilder(TaskBuilder, RuntimeEntityBuilderKubeaiserveSpeechtotext):
    """
    TaskKubeaiserveSpeechtotextServe builder.
    """

    ENTITY_CLASS = TaskKubeaiserveSpeechtotextServe
    ENTITY_SPEC_CLASS = TaskSpecKubeaiserveSpeechtotextServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorKubeaiserveSpeechtotextServe
    ENTITY_STATUS_CLASS = TaskStatusKubeaiserveSpeechtotextServe
    ENTITY_KIND = EntityKinds.TASK_KUBEAISERVESPEECHTOTEXT_SERVE.value
