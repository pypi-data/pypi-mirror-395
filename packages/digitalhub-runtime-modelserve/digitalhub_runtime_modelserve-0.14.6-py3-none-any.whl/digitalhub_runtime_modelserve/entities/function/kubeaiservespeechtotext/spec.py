# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_modelserve.entities.function.kubeaiserve.spec import (
    FunctionSpecKubeaiserve,
    FunctionValidatorKubeaiserve,
)


class FunctionSpecKubeaiserveSpeechtotext(FunctionSpecKubeaiserve):
    """
    FunctionSpecKubeaiserveSpeechtotext specifications.
    """


class FunctionValidatorKubeaiserveSpeechtotext(FunctionValidatorKubeaiserve):
    """
    FunctionValidatorKubeaiserveSpeechtotext validator.
    """
