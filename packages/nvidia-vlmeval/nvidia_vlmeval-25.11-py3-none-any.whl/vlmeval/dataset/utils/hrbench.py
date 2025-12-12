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

from ...smp import *
import os


def report_acc_hrbench(df):
    cycle_group = df.groupby('cycle_category')
    result_dic = defaultdict(list)
    avg_dic = defaultdict(int)

    count = 0
    for key, data_value in cycle_group:
        count += 1
        _, resp_dic = hrbench_score(data_value)

        for task_type, accuracy in resp_dic.items():
            result_dic['cycle'].append(key)
            result_dic['type'].append(task_type)
            result_dic['accuracy'].append(accuracy)

            avg_dic[task_type] += accuracy
    for task_type, accuracy in avg_dic.items():
        result_dic['cycle'].append('Average')
        result_dic['type'].append(task_type)
        result_dic['accuracy'].append(accuracy / count)
    result_pd = pd.DataFrame(result_dic)

    return result_pd


def hrbench_score(data):
    ret = defaultdict(list)
    resp_dic = {}
    category_list = set(data['category'])
    score_dict = defaultdict(list)

    for i in range(len(data)):
        d = data.iloc[i]
        category = d['category']
        gpt_score = d['hit']
        score_dict[category].append(gpt_score)
        score_dict['all'].append(gpt_score)

    all_acc = np.mean(score_dict['all'])
    ret['type'].append('all')
    ret['acc'].append(all_acc)
    resp_dic['all'] = all_acc
    for cate in category_list:
        acc = np.mean(score_dict[cate])
        ret['type'].append(cate)
        ret['acc'].append(acc)

        resp_dic[cate] = acc

    return pd.DataFrame(ret), resp_dic
