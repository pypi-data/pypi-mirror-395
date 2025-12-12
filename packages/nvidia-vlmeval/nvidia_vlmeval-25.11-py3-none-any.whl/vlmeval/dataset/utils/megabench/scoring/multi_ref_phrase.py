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

from numbers import Number
from .common.conversions import str_to_iterable
from .simple_str_match import SimpleStrMatch


def replace_potential_chinese_comma(input_string):
    return input_string.replace("，", ",")


class MultipleReferencePhraseEval:
    """
    Check the response with multiple correct references
    As long as one is matched, the score is 1, otherwise the score is 0
    """

    @staticmethod
    def match(response, targets) -> Number:
        targets = replace_potential_chinese_comma(targets)
        refs = str_to_iterable(list, targets)
        matched = False
        for ref in refs:
            str_ref = ref if isinstance(ref, str) else str(ref)
            if SimpleStrMatch.match(response, str_ref):
                matched = True
                break
        return 1 if matched else 0
