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

import ast


class PositiveIntMatch:
    """Positive int matching."""

    @staticmethod
    def match(response: str, correct_answer: str) -> int:
        """If the correct answer or response is a positive integer, then it returns if the predicted and correct answers are identical.

        Otherwise, it returns -1.
        """
        try:
            response_obj = ast.literal_eval(response)
        except (SyntaxError, ValueError):
            return 0

        if not correct_answer:
            return 0

        correct_answer_obj = ast.literal_eval(correct_answer)

        assert isinstance(correct_answer_obj, int)
        if not isinstance(response_obj, int):
            return 0

        # We only want to score the fields with a positive amount
        if correct_answer_obj <= 0 and response_obj <= 0:
            return -1

        return 1 if response_obj == correct_answer_obj else 0
