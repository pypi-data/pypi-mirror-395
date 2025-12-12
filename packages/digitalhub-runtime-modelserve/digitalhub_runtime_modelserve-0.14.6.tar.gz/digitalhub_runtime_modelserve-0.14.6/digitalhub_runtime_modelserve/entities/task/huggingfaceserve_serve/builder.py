# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderHuggingfaceserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.task.huggingfaceserve_serve.entity import TaskHuggingfaceserveServe
from digitalhub_runtime_modelserve.entities.task.huggingfaceserve_serve.spec import (
    TaskSpecHuggingfaceserveServe,
    TaskValidatorHuggingfaceserveServe,
)
from digitalhub_runtime_modelserve.entities.task.huggingfaceserve_serve.status import TaskStatusHuggingfaceserveServe


class TaskHuggingfaceserveServeBuilder(TaskBuilder, RuntimeEntityBuilderHuggingfaceserve):
    """
    TaskHuggingfaceserveServe builder.
    """

    ENTITY_CLASS = TaskHuggingfaceserveServe
    ENTITY_SPEC_CLASS = TaskSpecHuggingfaceserveServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorHuggingfaceserveServe
    ENTITY_STATUS_CLASS = TaskStatusHuggingfaceserveServe
    ENTITY_KIND = EntityKinds.TASK_HUGGINGFACESERVE_SERVE.value
