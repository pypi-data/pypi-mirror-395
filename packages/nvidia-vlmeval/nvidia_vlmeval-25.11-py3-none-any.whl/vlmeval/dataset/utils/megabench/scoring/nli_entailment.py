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

import torch
from transformers import pipeline


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pipe = pipeline(
    "text-classification", model="microsoft/deberta-large-mnli", device=device
)


class NliEntailment:
    """NLI entailment, where the correct answer is used as the premise."""

    @staticmethod
    def match(response, correct_answer) -> int:
        """Return whether the response and correct answer agree with each other."""
        if not isinstance(response, str) or isinstance(correct_answer, str):
            return 0
        resp = pipe(f"[CLS] {correct_answer.strip()} [SEP] {response.strip()} [SEP]")
        return 1 if resp[0]["label"] == "ENTAILMENT" else 0
