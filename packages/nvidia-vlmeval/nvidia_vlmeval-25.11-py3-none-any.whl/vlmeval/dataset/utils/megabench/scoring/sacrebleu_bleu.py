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

from numbers import Number
import sacrebleu


class Bleu:
    """Compute BLEU score, using SacreBLEU."""

    @staticmethod
    def match(response, correct_answer) -> Number:
        """Compute the BLEU scores between two strings."""
        if isinstance(response, str) and isinstance(correct_answer, str):
            resp = [response]
            corr = [correct_answer]
        elif isinstance(response, (list, tuple)) and isinstance(
            correct_answer, (list, tuple)
        ):
            resp = tuple(response)
            corr = tuple(correct_answer)
        else:
            return 0
        result = sacrebleu.corpus_bleu(corr, [resp]).score / 100
        return result
