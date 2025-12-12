# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.runtime_entity.builder import RuntimeEntityBuilder
from digitalhub.entities._commons.utils import map_actions

from digitalhub_runtime_modelserve.entities._commons.enums import Actions, EntityKinds


class RuntimeEntityBuilderMlflowserve(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_MLFLOWSERVE.value
    TASKS_KINDS = map_actions(
        [
            (
                EntityKinds.TASK_MLFLOWSERVE_SERVE.value,
                Actions.SERVE.value,
            ),
            (
                EntityKinds.TASK_MLFLOWSERVE_BUILD.value,
                Actions.BUILD.value,
            ),
        ]
    )
    RUN_KINDS = map_actions(
        [
            (
                EntityKinds.RUN_MLFLOWSERVE_SERVE.value,
                Actions.SERVE.value,
            ),
            (
                EntityKinds.RUN_MLFLOWSERVE_BUILD.value,
                Actions.BUILD.value,
            ),
        ]
    )


class RuntimeEntityBuilderHuggingfaceserve(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_HUGGINGFACESERVE.value
    TASKS_KINDS = map_actions(
        [
            (
                EntityKinds.TASK_HUGGINGFACESERVE_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )
    RUN_KINDS = map_actions(
        [
            (
                EntityKinds.RUN_HUGGINGFACESERVE_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )


class RuntimeEntityBuilderKubeaiserve(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_KUBEAISERVE.value
    TASKS_KINDS = map_actions(
        [
            (
                EntityKinds.TASK_KUBEAISERVE_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )
    RUN_KINDS = map_actions(
        [
            (
                EntityKinds.RUN_KUBEAISERVE_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )


class RuntimeEntityBuilderKubeaiserveSpeechtotext(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_KUBEAISERVESPEECHTOTEXT.value
    TASKS_KINDS = map_actions(
        [
            (
                EntityKinds.TASK_KUBEAISERVESPEECHTOTEXT_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )
    RUN_KINDS = map_actions(
        [
            (
                EntityKinds.RUN_KUBEAISERVESPEECHTOTEXT_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )


class RuntimeEntityBuilderKubeaiserveText(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_KUBEAISERVETEXT.value
    TASKS_KINDS = map_actions(
        [
            (
                EntityKinds.TASK_KUBEAISERVETEXT_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )
    RUN_KINDS = map_actions(
        [
            (
                EntityKinds.RUN_KUBEAISERVETEXT_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )


class RuntimeEntityBuilderSklearnserve(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_SKLEARNSERVE.value
    TASKS_KINDS = map_actions(
        [
            (
                EntityKinds.TASK_SKLEARNSERVE_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )
    RUN_KINDS = map_actions(
        [
            (
                EntityKinds.RUN_SKLEARNSERVE_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )
