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

from .kie_evaluator import KieEvaluator
from .doc_parsing_evaluator import ParsingEvaluator
from .ocr_evaluator import OcrEvaluator
from .common import summary


evaluator_map_info = {
    "kie": KieEvaluator("kie"),
    "doc_parsing": ParsingEvaluator("doc_parsing"),
    "multi_lan_ocr": OcrEvaluator("multi_lan_ocr"),
    "multi_scene_ocr": OcrEvaluator("multi_scene_ocr")
}
