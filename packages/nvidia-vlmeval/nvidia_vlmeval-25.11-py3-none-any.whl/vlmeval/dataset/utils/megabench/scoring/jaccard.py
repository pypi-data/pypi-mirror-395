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

from .common.conversions import cast_to_set
from .common.metrics import jaccard_index


class Jaccard:
    """Calculates the Jacard index for iterables."""

    @classmethod
    def match(cls, responses, targets) -> float:
        """Exact match between targets and responses."""
        if responses is None:
            return 0
        responses = cast_to_set(responses)
        targets = cast_to_set(targets)

        return jaccard_index(responses, targets)


class JaccardCaseInsensitive:
    """Calculates the Jacard index for iterables of strings,
    Do not consider the case
    """

    @classmethod
    def match(cls, responses, targets) -> float:
        """Exact match between targets and responses."""
        if responses is None:
            return 0
        responses = cast_to_set(responses)
        targets = cast_to_set(targets)

        if isinstance(list(targets)[0], str):
            new_responses = {
                item.lower() if isinstance(item, str) else str(item).lower()
                for item in responses
            }
            new_targets = {item.lower() for item in targets}
        elif isinstance(list(targets)[0], tuple):
            new_responses = set()
            new_targets = set()
            try:
                for res in responses:
                    new_res = tuple(
                        [
                            item.lower()
                            .replace(" ", "")
                            .replace("-", "")
                            .replace("\n", "")
                            .replace("\t", "")
                            .replace("_", "")
                            .replace(".", "")
                            for item in res
                        ]
                    )
                    new_responses.add(new_res)
            except:  # the data type of the response might be wrong, return 0 in this case
                return 0
            for tgt in targets:
                new_tgt = tuple(
                    [
                        item.lower()
                        .replace(" ", "")
                        .replace("-", "")
                        .replace("\n", "")
                        .replace("\t", "")
                        .replace("_", "")
                        .replace(".", "")
                        for item in tgt
                    ]
                )
                new_targets.add(new_tgt)
        else:
            return 0

        return jaccard_index(new_responses, new_targets)
