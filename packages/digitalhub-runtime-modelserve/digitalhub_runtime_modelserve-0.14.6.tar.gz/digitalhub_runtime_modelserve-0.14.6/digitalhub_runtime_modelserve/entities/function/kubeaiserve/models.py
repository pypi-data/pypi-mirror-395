# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class KubeaiAdapter(BaseModel):
    url: Optional[str] = None
    name: Optional[str] = None
