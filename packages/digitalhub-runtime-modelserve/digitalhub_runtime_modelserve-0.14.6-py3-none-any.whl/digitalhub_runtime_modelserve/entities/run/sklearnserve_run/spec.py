# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_modelserve.entities.run.modelserve_run.spec import (
    RunSpecModelserveRun,
    RunValidatorModelserveRun,
)


class RunSpecSklearnserveRun(RunSpecModelserveRun):
    """RunSpecSklearnserveRun specifications."""


class RunValidatorSklearnserveRun(RunValidatorModelserveRun):
    """RunValidatorSklearnserveRun validator."""
