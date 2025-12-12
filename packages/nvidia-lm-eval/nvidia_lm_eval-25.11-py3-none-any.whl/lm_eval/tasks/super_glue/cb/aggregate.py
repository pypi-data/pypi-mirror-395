# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

# Original Copyright EleutherAI.
# For the original license and copyright information, see the LICENSE file in this repository.

import numpy as np


def cb_multi_fi(items):
    from sklearn.metrics import f1_score

    preds, golds = zip(*items)
    preds = np.array(preds)
    golds = np.array(golds)
    f11 = f1_score(y_true=golds == 0, y_pred=preds == 0)
    f12 = f1_score(y_true=golds == 1, y_pred=preds == 1)
    f13 = f1_score(y_true=golds == 2, y_pred=preds == 2)
    avg_f1 = np.mean([f11, f12, f13])
    return avg_f1
