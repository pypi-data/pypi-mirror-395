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
# Original Copyright 2025 LiveCodeBench
# For the original license and copyright information, see the LICENSE file in this repository.

from livecodebench.lm_styles import LMStyle, LanguageModel


def build_runner(args, model: LanguageModel):
    if model.model_style in (LMStyle.OpenAIChat, LMStyle.GenericOAIServer):
        from livecodebench.runner.generic_oai_server_runner import GenericOAIServerRunner
        return GenericOAIServerRunner(args, model)
    
    if model.model_style in [LMStyle.OpenAIReason, LMStyle.OpenAIReasonPreview]:
        from livecodebench.runner.oai_runner import OpenAIRunner

        return OpenAIRunner(args, model)
    if model.model_style in [LMStyle.Gemini, LMStyle.GeminiThinking]:
        from livecodebench.runner.gemini_runner import GeminiRunner

        return GeminiRunner(args, model)
    if model.model_style == LMStyle.Claude3:
        from livecodebench.runner.claude3_runner import Claude3Runner

        return Claude3Runner(args, model)
    if model.model_style == LMStyle.Claude:
        from livecodebench.runner.claude_runner import ClaudeRunner

        return ClaudeRunner(args, model)
    if model.model_style == LMStyle.MistralWeb:
        from livecodebench.runner.mistral_runner import MistralRunner

        return MistralRunner(args, model)
    if model.model_style == LMStyle.CohereCommand:
        from livecodebench.runner.cohere_runner import CohereRunner

        return CohereRunner(args, model)
    if model.model_style == LMStyle.DeepSeekAPI:
        from livecodebench.runner.deepseek_runner import DeepSeekRunner

        return DeepSeekRunner(args, model)
    elif model.model_style in []:
        raise NotImplementedError(
            f"Runner for language model style {model.model_style} not implemented yet"
        )
    else:
        from livecodebench.runner.vllm_runner import VLLMRunner

        return VLLMRunner(args, model)
