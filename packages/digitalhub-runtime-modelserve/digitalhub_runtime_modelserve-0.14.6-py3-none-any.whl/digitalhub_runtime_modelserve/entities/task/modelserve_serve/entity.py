# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.task.modelserve_serve.spec import TaskSpecModelserveServe
    from digitalhub_runtime_modelserve.entities.task.modelserve_serve.status import TaskStatusModelserveServe


class TaskModelserveServe(Task):
    """
    TaskModelserveServe class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecModelserveServe,
        status: TaskStatusModelserveServe,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecModelserveServe
        self.status: TaskStatusModelserveServe
