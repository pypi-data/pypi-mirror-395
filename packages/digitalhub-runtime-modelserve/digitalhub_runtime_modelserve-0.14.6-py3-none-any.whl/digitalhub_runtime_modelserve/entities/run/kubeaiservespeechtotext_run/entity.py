# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.entity import RunKubeaiserveRun

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.run.kubeaiservespeechtotext_run.spec import (
        RunSpecKubeaiserveSpeechtotextRun,
    )
    from digitalhub_runtime_modelserve.entities.run.kubeaiservespeechtotext_run.status import (
        RunStatusKubeaiserveSpeechtotextRun,
    )


class RunKubeaiserveSpeechtotextRun(RunKubeaiserveRun):
    """
    RunKubeaiserveSpeechtotextRun class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecKubeaiserveSpeechtotextRun,
        status: RunStatusKubeaiserveSpeechtotextRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecKubeaiserveSpeechtotextRun
        self.status: RunStatusKubeaiserveSpeechtotextRun
