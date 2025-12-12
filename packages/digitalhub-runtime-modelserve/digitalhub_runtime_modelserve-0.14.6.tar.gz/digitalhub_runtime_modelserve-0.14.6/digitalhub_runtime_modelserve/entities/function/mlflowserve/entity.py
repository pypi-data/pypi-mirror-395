# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.function.modelserve.entity import FunctionModelserve

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.function.mlflowserve.spec import FunctionSpecMlflowserve
    from digitalhub_runtime_modelserve.entities.function.mlflowserve.status import FunctionStatusMlflowserve


class FunctionMlflowserve(FunctionModelserve):
    """
    FunctionMlflowserve class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpecMlflowserve,
        status: FunctionStatusMlflowserve,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpecMlflowserve
        self.status: FunctionStatusMlflowserve
