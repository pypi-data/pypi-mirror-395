# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderMlflowserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.task.mlflowserve_build.entity import TaskMlflowserveBuild
from digitalhub_runtime_modelserve.entities.task.mlflowserve_build.spec import (
    TaskSpecMlflowserveBuild,
    TaskValidatorMlflowserveBuild,
)
from digitalhub_runtime_modelserve.entities.task.mlflowserve_build.status import TaskStatusMlflowserveBuild


class TaskMlflowserveBuildBuilder(TaskBuilder, RuntimeEntityBuilderMlflowserve):
    """
    TaskMlflowserveBuild builder.
    """

    ENTITY_CLASS = TaskMlflowserveBuild
    ENTITY_SPEC_CLASS = TaskSpecMlflowserveBuild
    ENTITY_SPEC_VALIDATOR = TaskValidatorMlflowserveBuild
    ENTITY_STATUS_CLASS = TaskStatusMlflowserveBuild
    ENTITY_KIND = EntityKinds.TASK_MLFLOWSERVE_BUILD.value
