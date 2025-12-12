# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderKubeaiserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.task.kubeaiserve_serve.entity import TaskKubeaiserveServe
from digitalhub_runtime_modelserve.entities.task.kubeaiserve_serve.spec import (
    TaskSpecKubeaiserveServe,
    TaskValidatorKubeaiserveServe,
)
from digitalhub_runtime_modelserve.entities.task.kubeaiserve_serve.status import TaskStatusKubeaiserveServe


class TaskKubeaiserveServeBuilder(TaskBuilder, RuntimeEntityBuilderKubeaiserve):
    """
    TaskKubeaiserveServe builder.
    """

    ENTITY_CLASS = TaskKubeaiserveServe
    ENTITY_SPEC_CLASS = TaskSpecKubeaiserveServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorKubeaiserveServe
    ENTITY_STATUS_CLASS = TaskStatusKubeaiserveServe
    ENTITY_KIND = EntityKinds.TASK_KUBEAISERVE_SERVE.value
