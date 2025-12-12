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

import os
import json

from livecodebench.runner.parser import get_args
from livecodebench.utils.scenarios import Scenario
from livecodebench.utils.path_utils import get_output_path
from livecodebench.evaluation import extract_instance_results
from livecodebench.runner.scenario_router import (
    build_prompt_benchmark,
    sort_and_extract_save_results,
    get_metrics,
)


def main():
    args = get_args()

    benchmark, _ = build_prompt_benchmark(args)

    with open(args.custom_output_file, "r") as f:
        custom_outputs = json.load(f)
        assert isinstance(custom_outputs, list)
        assert len(custom_outputs) == len(benchmark), f"{len(custom_outputs)} != {len(benchmark)}"
        if isinstance(custom_outputs[0], list):
            ## custom outputs must list[list[str]]
            ## list of extracted outputs per question
            ## sorted by the benchmark question_id, test_id, id depending on the scenario

            assert all(
                isinstance(custom_output, list) for custom_output in custom_outputs
            )
        elif isinstance(custom_outputs[0], dict):
            ## custom outputs must list[dict[str, Any]]
            ## list of extracted outputs per question
            ## for codegeneration and selfrepair scenario -- `code_list` and `question_id` are required
            ## for testoutputprediction -- `pred_list`, `question_id`, `test_id` are required 
            ## for codeexecution -- `pred_list`, `id` are required 
            ## code_list/pred_list is a list of extracted answers (code or assertions) for a question

            assert all(
                isinstance(custom_output, dict) for custom_output in custom_outputs
            )
            if args.scenario in [Scenario.codegeneration, Scenario.selfrepair]:
                custom_outputs = [
                    custom_output["code_list"]
                    for custom_output in sorted(
                        custom_outputs, key=lambda x: str(x["question_id"])
                    )
                ]
            elif args.scenario == Scenario.testoutputprediction:
                custom_outputs = [
                    custom_output['pred_list']
                    for custom_output in sorted(
                        custom_outputs, key=lambda x: (str(x["question_id"]), str(x['test_id']))
                    )
                ]
            elif args.scenario == Scenario.codeexecution:
                custom_outputs = [
                    custom_output['pred_list']
                    for custom_output in sorted(
                        custom_outputs, key=lambda x: int(x.id.split("_")[1])
                    )
                ]

    save_results = [
        instance.insert_output(custom_output, custom_output)
        for instance, custom_output in zip(benchmark, custom_outputs)
    ]

    save_results, combined_results = sort_and_extract_save_results(
        args.scenario, save_results
    )

    metrics = get_metrics(args.scenario, args, benchmark, combined_results)
    graded = extract_instance_results(metrics[1])

    if args.scenario == Scenario.codegeneration:
        metadatas = metrics[2]
        save_eval_results = [
            instance.insert_output_evaluation(
                outputs_list, extracted_list, graded_list, metadata=meta
            )
            for instance, (outputs_list, extracted_list), graded_list, meta in zip(
                benchmark, combined_results, graded, metadatas
            )
        ]
    else:
        save_eval_results = [
            instance.insert_output_evaluation(
                outputs_list, extracted_list, graded_list
            )
            for instance, (outputs_list, extracted_list), graded_list in zip(
                benchmark, combined_results, graded
            )
        ]
    

    if args.custom_output_save_name is None:
        output_path = args.custom_output_file[:-5] + f"_{args.scenario.value}_output.json"
    else:
        output_path = get_output_path(args.custom_output_save_name, args)

    with open(output_path, "w") as f:
        json.dump(save_results, f, indent=4)


    with open(output_path.replace(".json", "_eval.json"), "w") as f:
        json.dump(metrics, f, indent=4)

    with open(output_path.replace(".json", "_eval_all.json"), "w") as f:
        json.dump(save_eval_results, f, indent=4)

if __name__ == "__main__":
    main()
