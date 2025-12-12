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
from .common.conversions import str_to_coords
import numpy as np


class CoordsSequenceSimilarity:
    """
    Measure the similarity between two list of coordinates, used for keypoint estimation tasks
    """

    @staticmethod
    def compute_score(pred_keypoints, gt_keypoints, k=10):
        """
        Compute the evaluation score for keypoint estimation.

        Args:
            pred_keypoints (list or np.ndarray): List or array of predicted keypoint coordinates,
                                                 each as (x, y), normalized to [0, 1].
            gt_keypoints (list or np.ndarray): List or array of ground truth keypoint coordinates,
                                               each as (x, y), normalized to [0, 1].

        Returns:
            float: A score between 0 and 1, where 1 indicates perfect accuracy,
                   and 0 indicates completely wrong.
        """
        # Convert inputs to NumPy arrays
        try:
            pred_keypoints = np.array(pred_keypoints)
        except ValueError:
            # Format is not a correct
            return 0

        gt_keypoints = np.array(gt_keypoints)

        # shape mismatch, directly assign 0 score
        if pred_keypoints.shape != gt_keypoints.shape:
            return 0

        # Compute Euclidean distances between corresponding keypoints
        distances = np.linalg.norm(pred_keypoints - gt_keypoints, axis=1)

        # Maximum possible distance in normalized coordinate space
        max_distance = np.sqrt(2)

        # Normalize distances
        normalized_distances = distances / max_distance

        # Compute per-keypoint scores using exponential decay
        per_keypoint_scores = np.exp(-k * normalized_distances)

        # Compute the average score across all keypoints
        score = np.mean(per_keypoint_scores)

        return score

    @classmethod
    def match(cls, responses, targets) -> float:
        """Exact match between targets and responses."""
        logging.debug(f"{responses=}, {targets=}")
        if not isinstance(responses, (tuple | list)):
            responses = str_to_coords(responses, dim=2)
        if not isinstance(targets, (tuple | list)):
            targets = str_to_coords(targets, dim=2)

        return cls.compute_score(responses, targets)
