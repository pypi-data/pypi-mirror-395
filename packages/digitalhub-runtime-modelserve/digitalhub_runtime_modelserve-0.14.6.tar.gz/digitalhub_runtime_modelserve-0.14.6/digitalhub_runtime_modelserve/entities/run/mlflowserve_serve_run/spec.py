# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import Field

from digitalhub_runtime_modelserve.entities.run.modelserve_run.spec import (
    RunSpecModelserveRun,
    RunValidatorModelserveRun,
)

path_regex = r"^(store://([^/]+)/model/mlflow/.*)" + r"|" + r".*\/$" + r"|" + r".*\.zip$"


class RunSpecMlflowserveServeRun(RunSpecModelserveRun):
    """RunSpecMlflowserveServeRun specifications."""


class RunValidatorMlflowserveServeRun(RunValidatorModelserveRun):
    """RunValidatorMlflowserveServeRun validator."""

    path: str = Field(default=None, pattern=path_regex)
