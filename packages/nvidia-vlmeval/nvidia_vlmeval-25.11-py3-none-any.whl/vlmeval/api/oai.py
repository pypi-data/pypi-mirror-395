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

import json
import os
import time
from pathlib import Path

import requests

from .gpt import OpenAIWrapper


class AzureOAIEndpoint(OpenAIWrapper):
    """Azure OpenAI API endpoint."""

    def __init__(
        self,
        model: str,
        retry: int = 5,
        wait: int = 5,
        verbose: bool = False,
        system_prompt: str = None,
        temperature: float = 0,
        top_p: float = 1.0,
        timeout: int = 60,
        max_tokens: int = 2048,
        img_size: int = 512,
        img_detail: str = "low",
        **kwargs,
    ):
        os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'] = model
        key = self._get_oauth_token()
        super().__init__(
            model=model,
            key=key,
            retry=retry,
            wait=wait,
            verbose=verbose,
            system_prompt=system_prompt,
            temperature=temperature,
            top_p=top_p,
            timeout=timeout,
            api_base=None,
            max_tokens=max_tokens,
            img_size=img_size,
            img_detail=img_detail,
            use_azure=True,
            **kwargs,
        )

    def generate_inner(self, inputs, **kwargs) -> str:
        ret_code, answer, response = super().generate_inner(inputs, **kwargs)
        # If the token is expired, get a new one and retry
        if ret_code in (401, 403):
            self.key = self._get_oauth_token()
            ret_code, answer, response = super().generate_inner(inputs, **kwargs)
        return ret_code, answer, response

    @staticmethod
    def _get_oauth_token(force: bool = False) -> str | None:
        required_vars = [
            "OPENAI_TOKEN_URL",
            "OPENAI_CLIENT_ID",
            "OPENAI_CLIENT_SECRET",
            "OPENAI_SCOPE",
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                "Azure environment variables missing: " + ", ".join(missing_vars)
            )

        p_token_url = os.environ.get("OPENAI_TOKEN_URL")
        p_client_id = os.environ.get("OPENAI_CLIENT_ID")
        p_client_secret = os.environ.get("OPENAI_CLIENT_SECRET")
        p_scope = os.environ.get("OPENAI_SCOPE")

        file_name = "py_llm_oauth_token.json"
        try:
            base_path = Path(__file__).parent
            file_path = Path.joinpath(base_path, file_name)
        except Exception as e:
            print(f"Error occurred while setting file path: {e}")
            return None

        try:
            # Check if the token is cached
            if not force and os.path.exists(file_path):
                with open(file_path, "r") as f:
                    token = json.load(f)
            else:
                # Get a new token from the OAuth server
                response = requests.post(
                    p_token_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": p_client_id,
                        "client_secret": p_client_secret,
                        "scope": p_scope,
                    },
                )
                response.raise_for_status()
                token = response.json()
                token["expires_at"] = time.time() + token["expires_in"]
                with open(file_path, "w") as f:
                    json.dump(token, f)
        except Exception as e:
            print(f"Error occurred while getting OAuth token: {e}")
            return None

        try:
            # Check if the token is expired
            if time.time() > token["expires_at"]:
                # Refresh the token
                if os.path.exists(file_path):
                    os.remove(file_path)
                return AzureOAIEndpoint._get_oauth_token()
        except Exception as e:
            print(f"Error occurred while getting OAuth token: {e}")
            return None

        return token["access_token"]


class CustomOAIEndpoint(OpenAIWrapper):
    """Custom OpenAI API compatible endpoint."""

    def __init__(
        self,
        model: str,
        api_base: str,
        api_key_var_name: str,
        retry: int = 5,
        wait: int = 5,
        verbose: bool = False,
        system_prompt: str = None,
        temperature: float = 0,
        top_p: float = 1.0,
        timeout: int = 60,
        max_tokens: int = 2048,
        img_size: int = 512,
        img_detail: str = "low",
        **kwargs,
    ):
        key = os.environ.get(api_key_var_name, "")
        super().__init__(
            model=model,
            api_base=api_base,
            key=key,
            retry=retry,
            wait=wait,
            verbose=verbose,
            system_prompt=system_prompt,
            temperature=temperature,
            top_p=top_p,
            timeout=timeout,
            max_tokens=max_tokens,
            img_size=img_size,
            img_detail=img_detail,
            use_azure=False,
            **kwargs,
        )
