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

import rapidfuzz
import unidecode
from .common.transformations import remove_def_indef_articles


def approximate(text: str) -> str:
    """Return an approximation of the original string."""
    return unidecode.unidecode(remove_def_indef_articles(text)).lower()


class NearStrMatch:
    """Near string matching."""

    @staticmethod
    def match(response, correct_answer: str, threshold=0.9) -> int:
        """Simple string match between response and correct_answer."""
        if not isinstance(response, str) or not isinstance(correct_answer, str):
            return 0
        response = approximate(response)
        correct_answer = approximate(correct_answer)
        return rapidfuzz.distance.DamerauLevenshtein.normalized_similarity(
            response, correct_answer, score_cutoff=threshold
        )
