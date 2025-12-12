# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class HuggingfaceTask(Enum):
    """
    Huggingface task name enum.
    """

    SEQUENCE_CLASSIFICATION = "sequence_classification"
    TOKEN_CLASSIFICATION = "token_classification"
    FILL_MASK = "fill_mask"
    TEXT_GENERATION = "text_generation"
    TEXT2TEXT_GENERATION = "text2text_generation"
    TEXT_EMBEDDING = "text_embedding"


class Backend(Enum):
    """
    Backend enum.
    """

    AUTO = "AUTO"
    VLLM = "VLLM"
    HUGGINGFACE = "HUGGINGFACE"


class Dtype(Enum):
    """
    Dtype enum.
    """

    AUTO = "AUTO"
    FLOAT32 = "FLOAT32"
    FLOAT16 = "FLOAT16"
    BFLOAT16 = "BFLOAT16"
    FLOAT = "FLOAT"
    HALF = "HALF"
