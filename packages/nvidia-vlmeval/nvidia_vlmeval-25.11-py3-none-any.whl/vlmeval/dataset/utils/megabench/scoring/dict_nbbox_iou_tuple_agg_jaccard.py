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

from .nbbox_iou import NbboxIouTuple


class DictNbboxIouTupleAggJaccard:
    """Calculates the average precision IoU across the dict.

    1. Calculates the precision IoU for all sets with the same key,
    if it appears in either pred or targets
    2. Calculates the total, then divides by the size of the union
    """

    @classmethod
    def match(cls, responses, targets) -> float:
        """Return the aggregated Jaccard index between targets and responses."""
        if not isinstance(responses, dict):
            return 0
        all_keys = set(responses) | set(targets)

        num_keys = 0
        total_score = 0
        for key in all_keys:
            total_score += NbboxIouTuple.match(
                responses.get(key, []), targets.get(key, [])
            )
            num_keys += 1

        return total_score / num_keys
