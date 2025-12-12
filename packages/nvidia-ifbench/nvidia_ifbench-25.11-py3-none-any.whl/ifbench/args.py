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

import argparse



class MisconfigurationError(Exception):
    pass



def comma_separated_to_dict(str_list: str, field_name: str) -> dict:
    if not str_list:
        return {}
    arg_list = str_list.split(",")
    arg_dict = {}
    for arg in arg_list:
        try:
            key, value = arg.split("=")
            try:
                value=int(value)
            except ValueError:
                try:
                    value=float(value)
                except:
                    pass
            arg_dict[key] = value
        except ValueError:
            raise MisconfigurationError(f"Incorrect parameters formatting for {field_name}")
    return arg_dict

def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Run inference on LLama Guard finetuned models"
    )

    parser.add_argument(
        "--model-url",
        type=str,
        help="Url to the model under test.",
        required=True,
    )


    parser.add_argument(
        "--model-name",
        type=str,
        help="Model name, as deployed.",
        required=True,
    )


    parser.add_argument(
        "--inference-params",
        type=str,
        help="""Comma-separated inference parameters for Model Under Test endpoint. E.g \"temperature=0,top_p=0.6\". " \
                These parameters are passed directly to OpenAI client. You can also provide additional parameters: 
                concurrency and retires which control behaviour but are not passed as a part of a payload""",
        default="",
        required=False
    )

    parser.add_argument(
        "--parallelism",
        type=int,
        help="Number of parallel calls",
        required=False,
        default=8,
    )

    parser.add_argument(
        "--retries",
        type=int,
        help="Number of retries",
        required=False,
        default=5,
    )

    parser.add_argument(
        "--results-dir", "-o", type=str, help="Results directory", required=True
    )

    parser.add_argument(
        "--limit", "-l", type=int, help="Limit number of samples to be evaluated", default=0, required=False
    )

    return parser
