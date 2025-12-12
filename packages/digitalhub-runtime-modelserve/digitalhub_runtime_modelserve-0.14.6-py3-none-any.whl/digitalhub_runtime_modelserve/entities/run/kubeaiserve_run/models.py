# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.enums import LoadBalancingStrategy


class KubeaiPrefixHash(BaseModel):
    mean_load_factor: Optional[int] = 125
    replication: Optional[int] = 256
    prefix_char_length: Optional[int] = 100


class LoadBalancing(BaseModel):
    strategy: Optional[LoadBalancingStrategy] = LoadBalancingStrategy.LEAST_LOAD.value
    prefix_hash: Optional[KubeaiPrefixHash] = KubeaiPrefixHash()


class Scaling(BaseModel):
    replicas: Optional[int] = 1
    min_replicas: Optional[int] = 1
    max_replicas: Optional[int] = None
    autoscaling_disabled: bool = False
    target_request: Optional[int] = 100
    scale_down_delay_seconds: Optional[int] = 30
    load_balancing: Optional[LoadBalancing] = None


class KubeaiFile(BaseModel):
    path: Optional[str] = None
    content: Optional[str] = None
