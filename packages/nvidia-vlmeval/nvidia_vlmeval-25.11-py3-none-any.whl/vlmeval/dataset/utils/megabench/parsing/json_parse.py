# SPDX-FileCopyrightText: Copyright 2023 VLMEvalKit Authors. All rights reserved.
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

from .common.parsers import parse_json
from .common.utils import evaluate_as_string


class JsonParse:
    """Load the response as a JSON object."""

    @staticmethod
    def parse(response: str):
        """Parse the JSON object, including nested JSON strings."""
        parsed_res = parse_json(response)
        # Drop the potentially duplicated string quotes
        if isinstance(parsed_res, dict):
            for key, val in parsed_res.items():
                parsed_res[key] = evaluate_as_string(val)

        return parsed_res
