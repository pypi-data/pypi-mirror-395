# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_modelserve.entities.task.kubeaiserve_serve.spec import (
    TaskSpecKubeaiserveServe,
    TaskValidatorKubeaiserveServe,
)


class TaskSpecKubeaiserveTextServe(TaskSpecKubeaiserveServe):
    """
    TaskSpecKubeaiserveTextServe specifications.
    """


class TaskValidatorKubeaiserveTextServe(TaskValidatorKubeaiserveServe):
    """
    TaskValidatorKubeaiserveTextServe validator.
    """
