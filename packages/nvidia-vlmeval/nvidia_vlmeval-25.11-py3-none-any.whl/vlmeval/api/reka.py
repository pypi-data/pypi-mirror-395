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

from vlmeval.smp import *
from vlmeval.api.base import BaseAPI
from time import sleep
import mimetypes


class Reka_Wrapper(BaseAPI):

    is_api: bool = True
    INTERLEAVE: bool = False

    def __init__(self,
                 model: str = 'reka-flash-20240226',
                 key: str = None,
                 retry: int = 10,
                 wait: int = 3,
                 system_prompt: str = None,
                 verbose: bool = True,
                 temperature: float = 0,
                 max_tokens: int = 1024,
                 **kwargs):

        try:
            import reka
        except ImportError:
            raise ImportError('Please install reka by running "pip install reka-api"')

        self.model = model
        default_kwargs = dict(temperature=temperature, request_output_len=max_tokens)
        default_kwargs.update(kwargs)
        self.kwargs = default_kwargs
        if key is not None:
            self.key = key
        else:
            self.key = os.environ.get('REKA_API_KEY', '')
        super().__init__(retry=retry, wait=wait, verbose=verbose, system_prompt=system_prompt, **kwargs)

    def generate_inner(self, inputs, **kwargs) -> str:
        import reka
        reka.API_KEY = self.key
        dataset = kwargs.pop('dataset', None)
        prompt, image_path = self.message_to_promptimg(inputs, dataset=dataset)
        image_b64 = encode_image_file_to_base64(image_path)

        response = reka.chat(
            model_name=self.model,
            human=prompt,
            media_url=f'data:image/jpeg;base64,{image_b64}',
            **self.kwargs)

        try:
            return 0, response['text'], response
        except Exception as err:
            return -1, self.fail_msg + str(err), response


class Reka(Reka_Wrapper):

    def generate(self, message, dataset=None):
        return super(Reka_Wrapper, self).generate(message)
