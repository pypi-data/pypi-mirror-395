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

# coding=utf-8
# Copyright 2025 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from langchain_core.runnables.config import RunnableConfig
from langchain_openai.chat_models.base import BaseChatOpenAI
import json
import os
import jsonlines
import os

import ifbench.evaluation_lib as evaluation_lib


from ifbench.callbacks import BatchCallback
from ifbench.args import build_arg_parser, comma_separated_to_dict
    

def run():
    parser = build_arg_parser()
    args = parser.parse_args()
    args.inference_params = comma_separated_to_dict(args.inference_params, "inference_params")
    args.model_url = args.model_url.rstrip("/chat/completions")

    model = BaseChatOpenAI(base_url=args.model_url, model=args.model_name, **args.inference_params)

    with open(os.path.join(os.path.dirname(__file__),'data/IFBench_test.jsonl'), 'r') as f:
        data = [json.loads(line)['prompt'] for line in f]
        if args.limit:
            data = data[:args.limit]

    with BatchCallback(len(data)) as cb:
        model_responses = model.with_retry(stop_after_attempt=args.retries).batch(data, config=RunnableConfig(max_concurrency=args.parallelism, callbacks=[cb]))
    model_responses = [response.content for response in model_responses]
    model_output = [{"prompt": prompt, "response": response} for prompt, response in zip(data, model_responses)]

    with jsonlines.open(os.path.join(args.results_dir, 'output.jsonl'), 'w') as writer:
        writer.write_all(model_output)

    inputs = evaluation_lib.read_prompt_list(os.path.join(os.path.dirname(__file__),'data/IFBench_test.jsonl')) # parametrize
    prompt_to_response = evaluation_lib.read_prompt_to_response_dict(
        os.path.join(args.results_dir, 'output.jsonl'))

    # get instruction following results
    all_metrics = {}
    for func, mode in [
        (evaluation_lib.test_instruction_following_strict, "strict"),
        (evaluation_lib.test_instruction_following_loose, "loose"),
    ]:
        output_file_name = f"eval_results_{mode}"
        print("Generating %s...", output_file_name) # unify logging
        outputs = []
        for inp in inputs:
            if (inp.prompt not in prompt_to_response) and args.limit:
                continue
            outputs.append(func(inp, prompt_to_response))
        follow_all_instructions = [o.follow_all_instructions for o in outputs]
        accuracy = sum(follow_all_instructions) / len(outputs)
        print("Accuracy: %f", accuracy)

        output_file_name = os.path.join(
            args.results_dir, output_file_name + ".jsonl"
        )
        evaluation_lib.write_outputs(output_file_name, outputs)
        print("Generated: %s", output_file_name) # unify logging

        # Prints instruction following accuracy report.
        print("=" * 64)
        print(f"{output_file_name} Accuracy Scores:")
        all_metrics |= evaluation_lib.generate_report(outputs, mode)
    
    with open(os.path.join(args.results_dir, "metrics.json"), "w") as outfile:
        outfile.write(json.dumps(all_metrics))



if __name__ == "__main__":
    run()
