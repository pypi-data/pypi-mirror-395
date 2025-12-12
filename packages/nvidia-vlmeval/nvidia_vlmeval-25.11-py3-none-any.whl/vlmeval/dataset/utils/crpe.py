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

import json
import argparse
from collections import defaultdict


def is_correct(predict, answer):
    # predict是标准答案 answer是预测
    if len(answer) == 1:
        return answer[0] == predict[0]
    elif len(answer) != 1 and answer[0] in ['A', 'B', 'C', 'D']:
        return answer[0] == predict[0]
    elif len(answer) != 1 and answer[0] not in ['A', 'B', 'C', 'D']:
        return predict[4:].lower() in answer.lower()
