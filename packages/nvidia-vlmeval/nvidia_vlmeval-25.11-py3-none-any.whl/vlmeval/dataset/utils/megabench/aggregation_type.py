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

from enum import Enum

class AggregationType(Enum):
    MEAN = 0

    @classmethod
    def from_string(cls, s):
        return cls.MEAN

    def aggregate(self, field_scores, field_weights):
        if not field_scores:
            return 0.0

        total_score = 0.0
        total_weight = 0.0

        for field, score in field_scores.items():
            weight = field_weights.get(field, 1.0)
            try:
                total_score += score * weight
            except:
                total_score += score[0] * weight
            total_weight += weight

        return total_score / total_weight if total_weight > 0 else 0.0
