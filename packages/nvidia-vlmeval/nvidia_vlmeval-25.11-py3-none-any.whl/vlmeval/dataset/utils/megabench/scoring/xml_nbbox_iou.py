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
from .common.metrics import calculate_iou
from .common.conversions import parse_bboxes_from_xml
from numbers import Number


class XmlNbboxIouSingle:
    """Calculates the IoU of bounding box.

    Assumes that co-ordinates are normalized between 0 and 1 and that the bounding boxes
    are of the form <box>top_left_x, top_left_y, bottom_right_x, bottom_right_y</box>
    """

    @classmethod
    def match(cls, responses, targets) -> float:

        logging.debug(f"{responses=}, {targets=}")
        if not isinstance(responses, (tuple | list)):
            responses = parse_bboxes_from_xml(responses)
        if not isinstance(targets, (tuple | list)):
            targets = parse_bboxes_from_xml(targets)

        if len(responses) == 0:
            return 0
        elif isinstance(responses[0], Number) and len(responses) == 4:
            responses = [responses]

        iou_scores = calculate_iou(responses, targets)
        if not iou_scores:
            return 0

        # Take the mean IoU score for now.
        return sum(iou_scores) / len(iou_scores)
