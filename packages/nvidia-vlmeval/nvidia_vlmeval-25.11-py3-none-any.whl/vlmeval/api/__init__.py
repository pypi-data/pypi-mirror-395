# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright 2023 VLMEvalKit Authors. All rights reserved.
# For the original license and copyright information, see the LICENSE file in this repository.

from .oai import AzureOAIEndpoint, CustomOAIEndpoint
from .gpt import OpenAIWrapper, GPT4V
from .hf_chat_model import HFChatModel
from .gemini import GeminiWrapper, GeminiProVision
from .qwen_vl_api import QwenVLWrapper, QwenVLAPI, Qwen2VLAPI
from .qwen_api import QwenAPI
from .claude import Claude_Wrapper, Claude3V
from .reka import Reka
from .glm_vision import GLMVisionAPI
from .cloudwalk import CWWrapper
from .sensechat_vision import SenseChatVisionAPI
from .siliconflow import SiliconFlowAPI, TeleMMAPI
from .hunyuan import HunyuanVision
from .bailingmm import bailingMMAPI
from .bluelm_v_api import BlueLMWrapper, BlueLM_V_API
from .jt_vl_chat import JTVLChatAPI
from .taiyi import TaiyiAPI
from .lmdeploy import LMDeployAPI
from .taichu import TaichuVLAPI, TaichuVLRAPI
from .doubao_vl_api import DoubaoVL
from .mug_u import MUGUAPI

__all__ = [
    "AzureOAIEndpoint",
    "CustomOAIEndpoint",
    "OpenAIWrapper",
    "HFChatModel",
    "GeminiWrapper",
    "GPT4V",
    "GeminiProVision",
    "QwenVLWrapper",
    "QwenVLAPI",
    "QwenAPI",
    "Claude3V",
    "Claude_Wrapper",
    "Reka",
    "GLMVisionAPI",
    "CWWrapper",
    "SenseChatVisionAPI",
    "HunyuanVision",
    "Qwen2VLAPI",
    "BlueLMWrapper",
    "BlueLM_V_API",
    "JTVLChatAPI",
    "bailingMMAPI",
    "TaiyiAPI",
    "TeleMMAPI",
    "SiliconFlowAPI",
    "LMDeployAPI",
    "TaichuVLAPI",
    "TaichuVLRAPI",
    "DoubaoVL",
    "MUGUAPI",
]
