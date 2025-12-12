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

from livecodebench.benchmarks.code_generation import (
    CodeGenerationProblem,
    load_code_generation_dataset,
    load_code_generation_dataset_not_fast,
)
from livecodebench.benchmarks.test_output_prediction import (
    TestOutputPredictionProblem,
    load_test_prediction_dataset,
)
from livecodebench.benchmarks.code_execution import (
    CodeExecutionProblem,
    load_code_execution_dataset,
)
