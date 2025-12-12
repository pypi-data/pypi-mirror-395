# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.function.modelserve.entity import FunctionModelserve

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.function.kubeaiserve.spec import FunctionSpecKubeaiserve
    from digitalhub_runtime_modelserve.entities.function.kubeaiserve.status import FunctionStatusKubeaiserve


class FunctionKubeaiserve(FunctionModelserve):
    """
    FunctionKubeaiserve class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpecKubeaiserve,
        status: FunctionStatusKubeaiserve,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpecKubeaiserve
        self.status: FunctionStatusKubeaiserve
