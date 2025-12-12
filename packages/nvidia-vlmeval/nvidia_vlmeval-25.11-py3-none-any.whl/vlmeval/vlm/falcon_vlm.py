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

from PIL import Image
import requests

from .base import BaseModel


class Falcon2VLM(BaseModel):

    INSTALL_REQ = False
    INTERLEAVE = False

    def __init__(self, model_path='tiiuae/falcon-11B-vlm', **kwargs):
        import torch
        from transformers import LlavaNextForConditionalGeneration, LlavaNextProcessor

        self.model_path = model_path
        self.processor = LlavaNextProcessor.from_pretrained(model_path, tokenizer_class='PreTrainedTokenizerFast')
        self.model = LlavaNextForConditionalGeneration.from_pretrained(
            model_path, torch_dtype=torch.bfloat16, device_map='cuda').eval()
        default_kwargs = {'max_new_tokens': 512}
        default_kwargs.update(kwargs)
        self.kwargs = default_kwargs

    def generate_inner(self, message, dataset=None):
        prompt, image_path = self.message_to_promptimg(message, dataset=dataset)
        image = Image.open(image_path).convert('RGB')

        prompt = f'User:<image>\n{prompt} Falcon:'
        inputs = self.processor(text=prompt, images=image, return_tensors='pt').to('cuda')

        output = self.model.generate(**inputs, **self.kwargs)
        prompt_length = inputs['input_ids'].shape[1]
        model_response = self.processor.decode(output[0][prompt_length:], skip_special_tokens=True).strip()
        return model_response
