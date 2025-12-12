# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from pydantic import Field

from digitalhub_runtime_modelserve.entities.run.modelserve_run.spec import (
    RunSpecModelserveRun,
    RunValidatorModelserveRun,
)

path_regex = r"^(store://([^/]+)/model/mlflow/.*)" + r"|" + r".*\/$" + r"|" + r".*\.zip$"


class RunSpecMlflowserveBuildRun(RunSpecModelserveRun):
    """RunSpecMlflowserveBuildRun specifications."""

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
        function: str | None = None,
        workflow: str | None = None,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list[dict] | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        runtime_class: str | None = None,
        priority_class: str | None = None,
        image: str | None = None,
        path: str | None = None,
        model_name: str | None = None,
        model_key: str | None = None,
        service_type: str | None = None,
        service_name: str | None = None,
        replicas: int | None = None,
        instructions: list[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            task,
            local_execution,
            function,
            workflow,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            runtime_class,
            priority_class,
            image,
            path,
            model_name,
            model_key,
            service_type,
            service_name,
            replicas,
            **kwargs,
        )
        self.instructions = instructions


class RunValidatorMlflowserveBuildRun(RunValidatorModelserveRun):
    """RunValidatorMlflowserveBuildRun validator."""

    path: str = Field(default=None, pattern=path_regex)

    instructions: Optional[list[str]] = None
