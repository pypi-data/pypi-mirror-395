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

"""caching utils
"""
import os

from evaluate import EvaluationModule


def update_hf_metric_lockfiles_permissions(metric: EvaluationModule) -> None:
    """By dfault hf metric create persistent .locks
    with permission granted only for user (640). This
    disables cache sharing.

    Args:
        metric (EvaluationModule): hf metric
    """
    if hasattr(metric, "filelocks"):
        for filelock in metric.filelocks:
            try:
                os.chmod(filelock.lock_file, 0o660)
            except FileNotFoundError:
                ...
