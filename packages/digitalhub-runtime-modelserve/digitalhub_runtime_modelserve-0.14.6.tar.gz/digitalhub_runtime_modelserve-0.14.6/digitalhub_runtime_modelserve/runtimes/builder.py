# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.runtimes.builder import RuntimeBuilder

from digitalhub_runtime_modelserve.runtimes.runtime import RuntimeModelserve


class RuntimeModelserveBuilder(RuntimeBuilder):
    """RuntaimeModelserveBuilder class."""

    RUNTIME_CLASS = RuntimeModelserve
