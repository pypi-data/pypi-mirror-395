# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.task.modelserve_serve.entity import TaskModelserveServe

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.task.kubeaiservetext_serve.spec import TaskSpecKubeaiserveTextServe
    from digitalhub_runtime_modelserve.entities.task.kubeaiservetext_serve.status import TaskStatusKubeaiserveTextServe


class TaskKubeaiserveTextServe(TaskModelserveServe):
    """
    TaskKubeaiserveTextServe class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecKubeaiserveTextServe,
        status: TaskStatusKubeaiserveTextServe,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecKubeaiserveTextServe
        self.status: TaskStatusKubeaiserveTextServe
