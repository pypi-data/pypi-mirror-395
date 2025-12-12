# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from digitalhub_runtime_modelserve.entities.task.modelserve_serve.spec import (
    TaskSpecModelserveServe,
    TaskValidatorModelserveServe,
)


class TaskSpecMlflowserveBuild(TaskSpecModelserveServe):
    """
    TaskSpecMlflowserveBuild specifications.
    """

    def __init__(
        self,
        function: str,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        replicas: int | None = None,
        service_type: str | None = None,
        service_name: str | None = None,
        instructions: list[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            volumes,
            resources,
            envs,
            secrets,
            profile,
            replicas,
            service_type,
            service_name,
            **kwargs,
        )
        self.instructions = instructions


class TaskValidatorMlflowserveBuild(TaskValidatorModelserveServe):
    """
    TaskValidatorMlflowserveBuild validator.
    """

    instructions: Optional[list[str]] = None
    """Instructions for the MLflow model serving build task."""
