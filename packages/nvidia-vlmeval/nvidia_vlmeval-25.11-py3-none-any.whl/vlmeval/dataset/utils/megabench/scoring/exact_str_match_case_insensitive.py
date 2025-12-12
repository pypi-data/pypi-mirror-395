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

from .exact_str_match import ExactStrMatch


class ExactStrMatchCaseInsensitive:
    """Case-insensitive exact string matching."""

    @staticmethod
    def match(response, correct_answer) -> int:
        """Case-insensitive exact match between targets and responses."""
        if not isinstance(response, str) and isinstance(correct_answer, str):
            return 0
        return ExactStrMatch.match(response.lower(), correct_answer.lower())
