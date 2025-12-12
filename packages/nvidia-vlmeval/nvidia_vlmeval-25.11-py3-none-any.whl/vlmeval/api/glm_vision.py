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

import requests
requests.packages.urllib3.disable_warnings()

from vlmeval.smp import *
from vlmeval.api.base import BaseAPI
from vlmeval.dataset import DATASET_TYPE
from vlmeval.smp.vlm import encode_image_file_to_base64


class GLMVisionWrapper(BaseAPI):

    is_api: bool = True

    def __init__(self,
                 model: str,
                 retry: int = 5,
                 wait: int = 5,
                 key: str = None,
                 verbose: bool = True,
                 system_prompt: str = None,
                 max_tokens: int = 4096,
                 proxy: str = None,
                 **kwargs):

        from zhipuai import ZhipuAI
        self.model = model
        self.fail_msg = 'Failed to obtain answer via API. '
        if key is None:
            key = os.environ.get('GLMV_API_KEY', None)
        assert key is not None, (
            'Please set the API Key (obtain it here: '
            'https://bigmodel.cn)'
        )
        self.client = ZhipuAI(api_key=key)
        super().__init__(wait=wait, retry=retry, system_prompt=system_prompt, verbose=verbose, **kwargs)

    def build_msgs(self, msgs_raw, system_prompt=None, dataset=None):
        msgs = cp.deepcopy(msgs_raw)
        content = []
        for i, msg in enumerate(msgs):
            if msg['type'] == 'text':
                content.append(dict(type='text', text=msg['value']))
            elif msg['type'] == 'image':
                content.append(dict(type='image_url', image_url=dict(url=encode_image_file_to_base64(msg['value']))))
        if dataset in {'HallusionBench', 'POPE'}:
            content.append(dict(type="text", text="Please answer yes or no."))
        ret = [dict(role='user', content=content)]
        return ret

    def generate_inner(self, inputs, **kwargs) -> str:
        assert isinstance(inputs, str) or isinstance(inputs, list)
        inputs = [inputs] if isinstance(inputs, str) else inputs

        messages = self.build_msgs(msgs_raw=inputs, dataset=kwargs.get('dataset', None))

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            do_sample=False,
            max_tokens=2048
        )
        try:
            answer = response.choices[0].message.content.strip()
            if self.verbose:
                self.logger.info(f'inputs: {inputs}\nanswer: {answer}')
            return 0, answer, 'Succeeded!'
        except Exception as err:
            if self.verbose:
                self.logger.error(f'{type(err)}: {err}')
                self.logger.error(f'The input messages are {inputs}.')
            return -1, self.fail_msg, ''


class GLMVisionAPI(GLMVisionWrapper):

    def generate(self, message, dataset=None):
        return super(GLMVisionAPI, self).generate(message, dataset=dataset)
