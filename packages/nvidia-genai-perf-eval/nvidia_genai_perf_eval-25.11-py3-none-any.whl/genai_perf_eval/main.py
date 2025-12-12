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

import subprocess
import os
import shutil
import argparse


def run_command(command, cwd=None):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd=cwd)

    _, stderr = process.communicate()
  
    if stderr:
        print(stderr.decode('utf-8', errors='replace'), end='', flush=True)

    rc = process.wait()
    if rc != 0:
        raise RuntimeError(f"Command {command} failed with return code {rc}")

    return rc

def run_eval(args):
    os.makedirs(args.artifact_dir, mode=0o777, exist_ok=True)
    concurrencies = args.concurrencies.split(',')
    headers = ""
    if args.endpoint_type == 'chat':
        args.endpoint = '/v1/chat/completions'
    elif args.endpoint_type == 'completions':
        args.endpoint = '/v1/completions'
    else:
        raise ValueError(f"Invalid endpoint type: {args.endpoint_type}")
    if args.api_key is not None:
        key = os.environ.get(args.api_key)
        if key is None:
            raise ValueError(f"API key {args.api_key} not found in environment variables")
        elif key == "":
            raise ValueError(f"API key {args.api_key} is empty")
        headers += rf'-H "Authorization: Bearer ${args.api_key}" '
    if "api.nvcf" in args.url:
        headers += f'-H "Accept: text/event-stream" '

    # Strip url from /v1/chat/completions, /v1/completions, /chat/completions, /completions
    args.url = args.url.replace(args.endpoint, '').lstrip('/')

    if args.warmup:
        concurrencies_to_run = [concurrencies[0]] + concurrencies
    else:
        concurrencies_to_run = concurrencies
    for concurrency in concurrencies_to_run:
        if args.run_only and f"{concurrency}_{args.isl}_{args.osl}" not in args.run_only:
            continue
        output_file = f"{args.model_id.lstrip('/').replace('/', '-')}_{args.endpoint_type}_{concurrency}_{args.isl}_{args.osl}"
        print(f"Running {output_file} creation")
        speed_command = f"genai-perf profile -m {args.model_id} "
        speed_command += f"--concurrency {concurrency} --tokenizer {args.tokenizer} "
        speed_command += f"--endpoint {args.endpoint} --endpoint-type {args.endpoint_type} --service-kind openai "
        if args.streaming:
            speed_command += f"--streaming "
        speed_command += f"-u {args.url} --num-prompts 100 "
        speed_command += f"--synthetic-input-tokens-mean {args.isl} --synthetic-input-tokens-stddev 0 --output-tokens-mean {args.osl} "
        speed_command += f"--extra-inputs max_tokens:{args.osl} --extra-inputs min_tokens:{args.osl} --extra-inputs ignore_eos:true "
        speed_command += f"--profile-export-file {output_file}.json --artifact-dir tmp/ "
        speed_command += f"--request-count {3*concurrency} -- --max-threads=1 {headers}"
        print(f"Running genai-perf cmd: {speed_command}")
        rc = run_command(speed_command)

        if not os.path.isfile(os.path.join("tmp", f"{output_file}.json")):
            print(f"Measurement failed for {output_file} with return code {rc}")
        else:
            src_path = os.path.join("tmp", f"{output_file}_genai_perf.json")
            dst_path = os.path.join(args.artifact_dir, f"{output_file}_genai_perf.json")
            shutil.copyfile(src_path, dst_path)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model_id', type=str, required=True, help='Id or name of the model being queried')
    parser.add_argument('--tokenizer', type=str, required=True, help='Tokenizer to use for the model')
    parser.add_argument('--url', type=str, required=False, help='url being queried', default="https://integrate.api.nvidia.com/v1")
    parser.add_argument('--endpoint-type', type=str, choices=['chat', 'completions'], required=False, help='endpoint type being queried', default='chat')
    parser.add_argument('--api-key', type=str, required=False, help='name of the variable that stores the API Key for endpoint if applicable', default=None)
    parser.add_argument('--concurrencies', type=str, required=True, help='Concurrencies to be used')

    parser.add_argument('--isl', type=str, required=True, help='ISL to be used')
    parser.add_argument('--osl', type=str, required=True, help='OSL to be used')

    parser.add_argument('--run-only', nargs="+", default=[], help='Run only the specified concurrency_isl_osl specified here, can be mulitple.')
    parser.add_argument('--artifact-dir', type=str, required=False, help='Directory where to store', default="artifacts")
    parser.add_argument('--warmup', action='store_true', default=False, help='Warmup the model before running the evaluation (run an extra eval with concurency=1)')
    parser.add_argument('--streaming', action='store_true', default=False, help='Run the evaluation in streaming mode')

    args = parser.parse_args()
    run_eval(args)