# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from digitalhub.entities.run._base.spec import RunSpec, RunValidator


class RunSpecModelserveRun(RunSpec):
    """RunSpecModelserveRun specifications."""

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
            **kwargs,
        )
        self.image = image
        self.path = path
        self.model_name = model_name
        self.model_key = model_key
        self.service_type = service_type
        self.service_name = service_name
        self.replicas = replicas


class RunValidatorModelserveRun(RunValidator):
    """RunValidatorModelserveRun Validator."""

    # Function parameters
    image: Optional[str] = None
    path: Optional[str] = None
    model_name: Optional[str] = None
    model_key: Optional[str] = None

    # Task serve
    service_type: Optional[str] = None
    service_name: Optional[str] = None
    replicas: Optional[int] = None
