# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderMlflowserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.task.mlflowserve_serve.entity import TaskMlflowserveServe
from digitalhub_runtime_modelserve.entities.task.mlflowserve_serve.spec import (
    TaskSpecMlflowserveServe,
    TaskValidatorMlflowserveServe,
)
from digitalhub_runtime_modelserve.entities.task.mlflowserve_serve.status import TaskStatusMlflowserveServe


class TaskMlflowserveServeBuilder(TaskBuilder, RuntimeEntityBuilderMlflowserve):
    """
    TaskMlflowserveServe builder.
    """

    ENTITY_CLASS = TaskMlflowserveServe
    ENTITY_SPEC_CLASS = TaskSpecMlflowserveServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorMlflowserveServe
    ENTITY_STATUS_CLASS = TaskStatusMlflowserveServe
    ENTITY_KIND = EntityKinds.TASK_MLFLOWSERVE_SERVE.value
