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
import os
import pathlib
import pty
import subprocess
from typing import Optional


def run_command(command, cwd=None):
    master, slave = pty.openpty()

    process = subprocess.Popen(
        command, stdout=slave, stderr=slave, stdin=subprocess.PIPE, cwd=cwd
    )
    os.close(slave)

    while True:
        try:
            output = os.read(master, 1024)
        except OSError:
            break
        if not output:
            break
        # `ignore` might lose bytes, don't use for anything critical
        print(output.decode(errors="ignore"), end="", flush=True)

    rc = process.wait()
    if rc != 0:
        raise RuntimeError(f"Command {command} failed with return code {rc}")

    return rc


def main():
    parser = argparse.ArgumentParser(
        description="Script for generating and judging results for Humanity's Last Exam."
    )

    # generation args
    parser.add_argument("--dataset", type=str, help="HLE HF Dataset")
    parser.add_argument("--model_name", type=str, help="Model Endpoint Name")
    parser.add_argument("--model_url", type=str, help="Model Endpoint URL")
    parser.add_argument(
        "--api_type",
        type=str,
        default="nvidia_api",
        choices=["azure", "openai", "nvidia_api"],
        help="Type of api",
    )
    parser.add_argument(
        "--api_key_name",
        type=str,
        help="API key env variable name (optional)",
        default=None,
    )
    parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=8192,
        help="Limit completion tokens. Recommended to avoid model collapse.",
    )
    parser.add_argument(
        "--temperature", type=float, default=0.0, help="Temperature for sampling."
    )
    parser.add_argument("--top_p", type=float, default=0.1, help="Top-p for sampling.")
    parser.add_argument(
        "--timeout", type=float, default=600.0, help="Timeout for sampling."
    )
    parser.add_argument(
        "--max_retries", type=int, default=1, help="Max retries for sampling."
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=100,
        help="Async semaphore size. This depends on your rate limit.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=os.path.join(pathlib.Path(__file__).parent, "results"),
        help="Folder where predictions and results are stored",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Use only the first --limit questions"
    )
    parser.add_argument(
        "--text_only", action="store_true", help="Omit image-based questions"
    )

    # judgement args
    parser.add_argument(
        "--predictions", type=str, default=None, help="Path to model predictions"
    )

    # other args
    parser.add_argument("--generate", action="store_true", help="Generate responses")
    parser.add_argument("--judge", action="store_true", help="Judge responses")

    args = parser.parse_args()

    if args.generate:
        print("Generation started")
        command = [
            "python",
            os.path.join(pathlib.Path(__file__).parent, "run_model_predictions.py"),
            "--dataset",
            args.dataset,
            "--model_name",
            args.model_name,
            "--model_url",
            args.model_url,
            "--api_type",
            args.api_type,
            "--api_key_name",
            str(args.api_key_name),
            "--max_new_tokens",
            str(args.max_new_tokens),
            "--temperature",
            str(args.temperature),
            "--top_p",
            str(args.top_p),
            "--timeout",
            str(args.timeout),
            "--max_retries",
            str(args.max_retries),
            "--num_workers",
            str(args.num_workers),
            "--output_dir",
            args.output_dir,
        ]

        if args.limit is not None:
            command.extend(["--limit", str(args.limit)])

        if args.text_only:
            command.append("--text_only")
        print(f"Run command: {' '.join(command)}")
        run_command(command)
        print("Generation complete")

    if args.judge:
        print("Judging started")
        if args.predictions is not None:
            predictions = args.predictions
        elif args.generate:
            model = args.model_name.replace("/", "-")
            predictions = os.path.join(args.output_dir, f"hle_{model}.json")
        else:
            raise ValueError("The path to the generated predictions is missing!")
        command = [
            "python",
            os.path.join(pathlib.Path(__file__).parent, "run_judge_results.py"),
            "--dataset",
            args.dataset,
            "--predictions",
            predictions,
            "--num_workers",
            str(args.num_workers),
            "--output_dir",
            args.output_dir,
        ]

        if args.text_only:
            command.append("--text_only")

        if args.limit is not None:
            command.extend(["--limit", str(args.limit)])

        print(f"Run command: {' '.join(command)}")
        run_command(command)
        print("Judging complete")


if __name__ == "__main__":
    main()
