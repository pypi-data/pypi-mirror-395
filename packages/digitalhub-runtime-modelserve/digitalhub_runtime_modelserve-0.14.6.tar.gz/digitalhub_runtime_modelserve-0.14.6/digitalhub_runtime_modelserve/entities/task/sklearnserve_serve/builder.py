# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderSklearnserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.task.sklearnserve_serve.entity import TaskSklearnserveServe
from digitalhub_runtime_modelserve.entities.task.sklearnserve_serve.spec import (
    TaskSpecSklearnserveServe,
    TaskValidatorSklearnserveServe,
)
from digitalhub_runtime_modelserve.entities.task.sklearnserve_serve.status import TaskStatusSklearnserveServe


class TaskSklearnserveServeBuilder(TaskBuilder, RuntimeEntityBuilderSklearnserve):
    """
    TaskSklearnserveServe builder.
    """

    ENTITY_CLASS = TaskSklearnserveServe
    ENTITY_SPEC_CLASS = TaskSpecSklearnserveServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorSklearnserveServe
    ENTITY_STATUS_CLASS = TaskStatusSklearnserveServe
    ENTITY_KIND = EntityKinds.TASK_SKLEARNSERVE_SERVE.value
