# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.function.modelserve.entity import FunctionModelserve

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.function.kubeaiservespeechtotext.spec import (
        FunctionSpecKubeaiserveSpeechtotext,
    )
    from digitalhub_runtime_modelserve.entities.function.kubeaiservespeechtotext.status import (
        FunctionStatusKubeaiserveSpeechtotext,
    )


class FunctionKubeaiserveSpeechtotext(FunctionModelserve):
    """
    FunctionKubeaiserveSpeechtotext class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpecKubeaiserveSpeechtotext,
        status: FunctionStatusKubeaiserveSpeechtotext,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpecKubeaiserveSpeechtotext
        self.status: FunctionStatusKubeaiserveSpeechtotext
