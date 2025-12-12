# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class LoadBalancingStrategy(Enum):
    LEAST_LOAD = "LeastLoad"
    PREFIX_HASH = "PrefixHash"
