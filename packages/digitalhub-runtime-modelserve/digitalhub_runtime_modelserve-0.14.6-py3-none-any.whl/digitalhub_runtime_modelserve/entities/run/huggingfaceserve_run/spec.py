# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from digitalhub_runtime_modelserve.entities.run.modelserve_run.spec import (
    RunSpecModelserveRun,
    RunValidatorModelserveRun,
)
from digitalhub_runtime_modelserve.entities.task.huggingfaceserve_serve.models import Backend, Dtype, HuggingfaceTask


class RunSpecHuggingfaceserveRun(RunSpecModelserveRun):
    """RunSpecHuggingfaceserveRun specifications."""

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
        replicas: int | None = None,
        huggingface_task: str | None = None,
        backend: str | None = None,
        tokenizer_revision: str | None = None,
        max_length: int | None = None,
        disable_lower_case: bool | None = None,
        disable_special_tokens: bool | None = None,
        Dtype: str | None = None,
        trust_remote_code: bool | None = None,
        tensor_input_names: list[str] | None = None,
        return_token_type_ids: bool | None = None,
        return_probabilities: bool | None = None,
        args: list[str] | None = None,
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
            replicas,
            **kwargs,
        )
        self.huggingface_task = huggingface_task
        self.backend = backend
        self.tokenizer_revision = tokenizer_revision
        self.max_length = max_length
        self.disable_lower_case = disable_lower_case
        self.disable_special_tokens = disable_special_tokens
        self.Dtype = Dtype
        self.trust_remote_code = trust_remote_code
        self.tensor_input_names = tensor_input_names
        self.return_token_type_ids = return_token_type_ids
        self.return_probabilities = return_probabilities
        self.args = args


class RunValidatorHuggingfaceserveRun(RunValidatorModelserveRun):
    """RunValidatorHuggingfaceserveRun validator."""

    # Task parameters
    huggingface_task: Optional[HuggingfaceTask] = None
    backend: Optional[Backend] = None
    tokenizer_revision: str = None
    max_length: int = None
    disable_lower_case: bool = None
    disable_special_tokens: bool = None
    Dtype: Optional[Dtype] = None
    trust_remote_code: bool = None
    tensor_input_names: list[str] = None
    return_token_type_ids: bool = None
    return_probabilities: bool = None
    disable_log_requests: bool = None
    max_log_len: int = None

    # Run parameters
    args: list[str] = None
    """Arguments for the huggingface serve command."""
