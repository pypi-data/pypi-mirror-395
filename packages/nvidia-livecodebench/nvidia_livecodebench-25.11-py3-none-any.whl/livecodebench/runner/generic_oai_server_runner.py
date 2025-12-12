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

import os
import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

from livecodebench.runner.base_runner import BaseRunner
from livecodebench.utils.seed_generator import SeedGenerator

logger = logging.getLogger(__name__)


class GenericOAIServerRunner(BaseRunner):
    def __init__(self, args, model):
        super().__init__(args, model)
        self.url = args.url or "https://api.openai.com/v1/chat/completions"
        self.api_key = os.getenv("API_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.timeout = getattr(args, "timeout")
        self.max_retries = getattr(args, "max_retries")
        self.support_system_role = args.support_system_role
        self.client_kwargs = {
            "model": args.model,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "top_p": args.top_p,
        }
        self.seed_generator = SeedGenerator()

    @staticmethod
    def remove_sys_role(messages: list[dict[str, str]]) -> list[dict[str, str]]:
        if messages[0]["role"] == "system":
            sys_msg, first_msg, *remaining = messages
            first_msg = {
                "role": "user",
                "content": sys_msg["content"] + "\n" + first_msg["content"],
            }
            messages = [first_msg] + remaining
        return messages

    def _make_request_internal(self, payload):
        """Internal method to send request to OpenAI API."""
        response = requests.post(
            self.url, headers=self.headers, json=payload, timeout=self.timeout
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        response_data = response.json()
        responses = []
        for choice in response_data.get("choices"):
            content = choice["message"]["content"] or ""
            responses.append(content)
        return responses

    def _make_request(self, payload):
        """Send the request with retries and log each retry attempt."""

        def _after_retry(retry_state):
            exc = retry_state.outcome.exception()
            attempt = retry_state.attempt_number
            msg = (
                f"{type(exc).__name__}: {exc}" if exc else "Unknown error"
            )
            logger.warning(
                "Retry attempt %d/%d for URL %s failed → %s",
                attempt,
                self.max_retries,
                self.url,
                msg,
            )

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=2, min=2, max=5),
            after=_after_retry,
            reraise=True,
        )
        def _retry_request():
            return self._make_request_internal(payload)

        return _retry_request()

    def _run_single(self, prompt: list[dict[str, str]], idx: int = 0) -> list[str]:
        assert isinstance(prompt, list)
        if not self.support_system_role:
            prompt = self.remove_sys_role(prompt)
        outputs = []
        for i in range(self.args.n):
            seed = self.seed_generator.get_seed(idx, i)
            payload = {"messages": prompt, **self.client_kwargs, "seed": seed}
            outputs.extend(self._make_request(payload))
        return outputs
