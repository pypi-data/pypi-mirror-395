# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class EntityKinds(Enum):
    """
    Entity kinds.
    """

    FUNCTION_HUGGINGFACESERVE = "huggingfaceserve"
    TASK_HUGGINGFACESERVE_SERVE = "huggingfaceserve+serve"
    RUN_HUGGINGFACESERVE_SERVE = "huggingfaceserve+serve:run"

    FUNCTION_MLFLOWSERVE = "mlflowserve"
    TASK_MLFLOWSERVE_BUILD = "mlflowserve+build"
    RUN_MLFLOWSERVE_BUILD = "mlflowserve+build:run"
    TASK_MLFLOWSERVE_SERVE = "mlflowserve+serve"
    RUN_MLFLOWSERVE_SERVE = "mlflowserve+serve:run"

    FUNCTION_SKLEARNSERVE = "sklearnserve"
    TASK_SKLEARNSERVE_SERVE = "sklearnserve+serve"
    RUN_SKLEARNSERVE_SERVE = "sklearnserve+serve:run"

    FUNCTION_KUBEAISERVE = "kubeaiserve"
    TASK_KUBEAISERVE_SERVE = "kubeaiserve+serve"
    RUN_KUBEAISERVE_SERVE = "kubeaiserve+serve:run"

    FUNCTION_KUBEAISERVETEXT = "kubeai-text"
    TASK_KUBEAISERVETEXT_SERVE = "kubeai-text+serve"
    RUN_KUBEAISERVETEXT_SERVE = "kubeai-text+serve:run"

    FUNCTION_KUBEAISERVESPEECHTOTEXT = "kubeai-speech"
    TASK_KUBEAISERVESPEECHTOTEXT_SERVE = "kubeai-speech+serve"
    RUN_KUBEAISERVESPEECHTOTEXT_SERVE = "kubeai-speech+serve:run"


class Actions(Enum):
    """
    Task actions.
    """

    SERVE = "serve"
    BUILD = "build"
