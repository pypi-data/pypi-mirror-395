# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from digitalhub.entities.run._base.spec import RunSpec, RunValidator
from pydantic import Field

from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.models import KubeaiFile, Scaling


class RunSpecKubeaiserveRun(RunSpec):
    """RunSpecKubeaiserveRun specifications."""

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
        model_name: str | None = None,
        url: str | None = None,
        image: str | None = None,
        adapters: list[dict] | None = None,
        processors: int | None = None,
        env: dict | None = None,
        args: list[str] | None = None,
        cache_profile: str | None = None,
        scaling: dict | None = None,
        files: list[dict] | None = None,
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
        )
        self.model_name = model_name
        self.url = url
        self.image = image
        self.adapters = adapters
        self.processors = processors
        self.env = env
        self.args = args
        self.cache_profile = cache_profile
        self.scaling = scaling
        self.files = files


class RunValidatorKubeaiserveRun(RunValidator):
    """RunValidatorKubeaiserveRun validator."""

    # Function parameters
    model_name: Optional[str] = None
    image: Optional[str] = None
    url: Optional[str] = None
    adapters: Optional[list[dict]] = None

    # Run parameters
    processors: Optional[int] = Field(default=None, ge=1)
    "Number of processors."

    env: Optional[dict] = None
    """Environment variables."""

    args: Optional[list[str]] = None
    """Arguments."""

    cache_profile: Optional[str] = None
    """Cache profile."""

    files: Optional[list[KubeaiFile]] = None
    """Files."""

    scaling: Optional[Scaling] = None
    """Scaling parameters."""
