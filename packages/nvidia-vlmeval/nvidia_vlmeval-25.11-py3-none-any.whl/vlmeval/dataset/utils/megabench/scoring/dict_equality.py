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

from .common.conversions import cast_to_dict
from .simple_str_match import ExactStrMatch


class DictEquality:
    """Calculates the exact string match across the dict.

    1. Calculates the exact match for all keys in the solution
    2. Calculates the total, then divides by the size of the solution
    """

    @classmethod
    def match(cls, responses, targets) -> float:
        """Return the aggregated Jaccard index between targets and responses."""
        responses = cast_to_dict(responses)
        targets = cast_to_dict(targets)

        if not isinstance(responses, dict):
            return 0

        return 1 if responses == targets else 0


class DictPrecision:

    @classmethod
    def match(cls, responses, targets) -> float:
        """Return the aggregated Jaccard index between targets and responses."""
        responses = cast_to_dict(responses)
        targets = cast_to_dict(targets)

        if not isinstance(responses, dict):
            return 0

        if len(responses) == 0:
            return 0

        matched = 0
        for key, val in responses.items():
            if key in targets:
                if ExactStrMatch.match(val, targets[key]):
                    matched += 1

        return matched / len(responses)
