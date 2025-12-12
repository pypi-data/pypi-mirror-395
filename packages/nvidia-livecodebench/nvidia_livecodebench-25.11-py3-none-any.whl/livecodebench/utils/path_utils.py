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
#
# Original Copyright 2025 LiveCodeBench
# For the original license and copyright information, see the LICENSE file in this repository.

import pathlib

from livecodebench.lm_styles import LanguageModel, LMStyle
from livecodebench.utils.scenarios import Scenario


def ensure_dir(path: str, is_file=True):
    if is_file:
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    else:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return


def get_output_file_name(model_repr:str, args, suffix: str = "") -> str:
    scenario: Scenario = args.scenario
    n = args.n
    cot_suffix = "_cot" if args.cot_code_execution else ""
    release_version = args.release_version
    return f"{model_repr}_{scenario}_{release_version}_{n}_{cot_suffix}{suffix}.json"

def get_cache_path(model_repr:str, args) -> str:
    out_file = get_output_file_name(model_repr, args)
    path = f"{args.out_dir}/cache/{out_file}"
    ensure_dir(path)
    return path


def get_output_path(model_repr:str, args) -> str:
    out_file = get_output_file_name(model_repr, args)
    path = f"{args.out_dir}/{out_file}"
    ensure_dir(path)
    return path


def get_eval_all_output_path(model_repr:str, args) -> str:
    out_file = get_output_file_name(model_repr, args, suffix="_eval_all.json")
    path = f"{args.out_dir}/output/{out_file}"
    ensure_dir(path)
    return path
