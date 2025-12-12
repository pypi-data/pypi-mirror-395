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

import logging
from typing import Dict, Any
from .common.conversions import str_to_set
from .common.metrics import jaccard_index


def chess_transform(move_sequence: str) -> set:
    """Transform a sequence of chess moves encoded in SAN into a set."""
    move_sequence = str_to_set(move_sequence)
    return {move_san.removesuffix("!").removesuffix("#") for move_san in move_sequence}


class ChessMoveJaccard:
    """Calculates the Jacard index for chess moves."""

    @classmethod
    def match(cls, responses: str | None, targets: str) -> float:
        """Exact match between targets and responses."""
        if responses is None:
            return 0
        responses = chess_transform(responses)
        targets = chess_transform(targets)

        return jaccard_index(responses, targets)
