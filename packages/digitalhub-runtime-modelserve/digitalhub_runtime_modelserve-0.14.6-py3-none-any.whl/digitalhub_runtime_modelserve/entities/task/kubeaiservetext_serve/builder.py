# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderKubeaiserveText
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.task.kubeaiservetext_serve.entity import TaskKubeaiserveTextServe
from digitalhub_runtime_modelserve.entities.task.kubeaiservetext_serve.spec import (
    TaskSpecKubeaiserveTextServe,
    TaskValidatorKubeaiserveTextServe,
)
from digitalhub_runtime_modelserve.entities.task.kubeaiservetext_serve.status import TaskStatusKubeaiserveTextServe


class TaskKubeaiserveTextServeBuilder(TaskBuilder, RuntimeEntityBuilderKubeaiserveText):
    """
    TaskKubeaiserveTextServe builder.
    """

    ENTITY_CLASS = TaskKubeaiserveTextServe
    ENTITY_SPEC_CLASS = TaskSpecKubeaiserveTextServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorKubeaiserveTextServe
    ENTITY_STATUS_CLASS = TaskStatusKubeaiserveTextServe
    ENTITY_KIND = EntityKinds.TASK_KUBEAISERVETEXT_SERVE.value
