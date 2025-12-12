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

from .judge_util import build_judge, DEBUG_MESSAGE
from .multiple_choice import extract_answer_from_item, prefetch_answer
from .vqa_eval import levenshtein_distance


__all__ = [
    'build_judge', 'extract_answer_from_item', 'prefetch_answer',
    'levenshtein_distance', 'DEBUG_MESSAGE',
]
