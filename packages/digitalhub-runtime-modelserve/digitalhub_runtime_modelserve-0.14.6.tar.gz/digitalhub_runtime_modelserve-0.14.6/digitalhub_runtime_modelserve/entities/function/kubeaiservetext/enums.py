# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class KubeaiEngine(Enum):
    OLLAMA = "OLlama"
    VLLM = "VLLM"
    FASTER_WHISPER = "FasterWhisper"
    INFINITY = "Infinity"


class KubeaiFeature(Enum):
    TEXT_GENERATION = "TextGeneration"
    TEXT_EMBEDDING = "TextEmbedding"
    SPEECH_TO_TEXT = "SpeechToText"
