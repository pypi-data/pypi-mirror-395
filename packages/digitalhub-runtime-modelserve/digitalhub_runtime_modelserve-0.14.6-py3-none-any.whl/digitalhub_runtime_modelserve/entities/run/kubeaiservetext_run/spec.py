# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.spec import (
    RunSpecKubeaiserveRun,
    RunValidatorKubeaiserveRun,
)


class RunSpecKubeaiserveTextRun(RunSpecKubeaiserveRun):
    """RunSpecKubeaiserveTextRun specifications."""

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
        features: list[str] | None = None,
        engine: str | None = None,
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
            model_name,
            url,
            image,
            adapters,
            processors,
            env,
            args,
            cache_profile,
            scaling,
            files,
        )
        self.features = features
        self.engine = engine


class RunValidatorKubeaiserveTextRun(RunValidatorKubeaiserveRun):
    """RunValidatorKubeaiserveTextRun validator."""

    features: Optional[list[str]] = None
    engine: Optional[str] = None
