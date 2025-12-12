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
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
from functools import partial
from importlib import resources
import json
from omegaconf import OmegaConf
import subprocess
import time
import shutil
import numpy as np
from pathlib import Path
from typing import Optional

from scicode.data.downloader import download_test_data
from scicode.gen.gencode_json import Gencode
from scicode.parse.parse import H5PY_FILE, read_from_jsonl


DEFAULT_PROMPT_TEMPLATE = resources.read_text("scicode.data", "background_comment_template.txt")
BACKGOUND_PROMPT_TEMPLATE = resources.read_text("scicode.data", "multistep_template.txt")

with resources.path("scicode.data", "problems_all.jsonl") as p:
    INPUT_JSON_PATH = p
with resources.path("scicode.data", "problems_dev.jsonl") as p:
    DEV_JSON_PATH = p


def extra_params(args_string: str) -> dict:
    """
    Parses something like
        args1=val1,arg2=val2
    Into a dictionary
    """
    args_string = args_string.strip()
    if not args_string:
        return {}
    arg_list = args_string.split(",")
    args_dict = OmegaConf.to_object(OmegaConf.from_dotlist(arg_list))
    return args_dict


def get_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
    )
    parser.add_argument(
        "--model", type=str, required=True, help="Model name"
    )
    parser.add_argument(
        "--url", type=str, required=True, help="Endpoint url (full)")

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("eval_results"),
        help="Output directory",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=Path("logs"),
        help="Log directory",
    )
    parser.add_argument(
        "--with-background",
        action="store_true",
        help="Include problem background if enabled",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0,
        help="Generation temperature",
    )
    parser.add_argument(
        "--limit-samples",
        type=int,
        default=None,
        help="Use only first N problems",
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        default=1,
        help="Generate N responses for each prompt",
    )
    parser.add_argument(
        "--extra-params",
        type=extra_params,
        default=None,
        help="Additional params passed to the inference function",
    )
    parser.add_argument(
        "--include-dev",
        action="store_true",
        help="Include dev problems",
    )
    parser.add_argument(
        "--eval-threads",
        type=int,
        default=None,
        help="Number of threads to use for evaluation. If not provided, uses all available CPUs",
    )
    parser.add_argument(
        "--concurrent-requests",
        type=int,
        default=1,
        help="Number of concurrent requests to send to the model.",
    )
    return parser


def _get_background_dir(with_background):
    return "with_background" if with_background else "without_background"

def estimate_pass_at_k(num_samples, num_correct, k=1):
    """Estimates pass@k"""

    if num_samples - num_correct < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(num_samples - num_correct + 1, num_samples + 1))



def test_code(model_name, code_dir, log_dir, output_dir,
              jsonl_data, with_background=False, n_samples: int = 1,
              eval_threads: Optional[int] = None):

    json_idx = {}

    steps_per_prob = defaultdict(int)
    correct_per_prob = defaultdict(lambda: defaultdict(int))

    for prob_data in jsonl_data:
        steps_per_prob[prob_data['problem_id']] += len(prob_data['sub_steps'])
        json_idx[prob_data['problem_id']] = jsonl_data.index(prob_data)
        if prob_data['problem_id'] in ("13", "62", "76"):
            # for these 3 problems one step is skiped and we need to account for that
            steps_per_prob[prob_data['problem_id']] -= 1

    start_time = time.time()

    code_dir_ = Path(code_dir, model_name, _get_background_dir(with_background))
    tmp_dir = Path(f'tmp_{start_time}')

    tmp_dir.mkdir(parents=True, exist_ok=True)

    for file_path in code_dir_.iterdir():
        if file_path.is_file():
            file_name = file_path.stem
            file_id = file_name.split(".")[0]
            file_step, repeat_num = file_name.split(".")[1].split('_')

            code_content = file_path.read_text(encoding='utf-8')
            json_content = jsonl_data[json_idx[file_id]]
            step_id = json_content["sub_steps"][int(file_step) - 1]["step_number"]
            test_lst = json_content["sub_steps"][int(file_step) - 1]["test_cases"]
            assert_file = Path(tmp_dir, f'{step_id}_{repeat_num}.py')
            with open(assert_file, 'w', encoding='utf-8') as f:
                f.write(code_content)
                f.write(f"""

from scicode.parse.parse import process_hdf5_to_tuple

""")
                f.write(f"targets = process_hdf5_to_tuple('{step_id}', {len(test_lst)})" + '\n')
                for idx in range(len(test_lst)):
                    f.write(f"target = targets[{idx}]\n\n")
                    for line in test_lst[idx].split('\n'):
                        f.write(line + '\n')

    logs_dir_ = Path(log_dir, model_name, _get_background_dir(with_background))
    logs_dir_.mkdir(parents=True, exist_ok=True)

    def check_script(script_path, logs_dir):
        logs_file = Path(logs_dir, f'{script_path.stem}.txt')

        if logs_file.exists():
            with open(logs_file, 'r') as f:
                content = f.read().splitlines()
                if content[0] == 'pass':
                    return True
        try:
            subprocess.run(['python', script_path], check=True, capture_output=True,
                           text=True, timeout=1800)
            result = 'pass'
        except subprocess.CalledProcessError as e:
            print(f"Error running script {script_path}: {e}")
            print(e.output)
            result = 'fail'
        except subprocess.TimeoutExpired as e:
            print(f"Runtime error while running script {script_path}: {e}")
            result = 'time out'

        with open(logs_file, 'w') as f:
            f.write(result)
        return result == 'pass'


    files_to_check = [file_path for file_path in tmp_dir.iterdir() if file_path.is_file()]
    with ThreadPoolExecutor(max_workers=eval_threads) as executor:
        tests_passing = list(executor.map(partial(check_script, logs_dir=logs_dir_), files_to_check))
    assert len(files_to_check) == len(tests_passing), f"got {tests_passing} results for {files_to_check} scripts"

    for file_path, is_passing in zip(files_to_check, tests_passing):
        func_id = file_path.stem
        prob_id = func_id.split('.')[0]
        step_id, repeat_num = func_id.split(".")[1].split('_')
        if is_passing:
            correct_per_prob[prob_id][step_id] += 1

    test_time = time.time() - start_time

    per_prob_pass = []
    per_step_pass = []
    for prob_id, num_steps in steps_per_prob.items():
        prob_score = 1
        for i in range(num_steps):
            if (prob_id == 13 and i == 5) or (prob_id == 62 and i == 0)\
                    or (prob_id == 76 and i == 2):
                continue
            num_correct = correct_per_prob[str(prob_id)][str(i + 1)]
            pass_at_1 = estimate_pass_at_k(num_samples=n_samples, num_correct=num_correct, k=1)
            # we multiply probabilities to estimate prob that all steps are correct
            # FIXME(martas) we falsely assume that each substep is independent here but I don't have a better idea
            prob_score *= pass_at_1
            per_step_pass.append(pass_at_1)
        per_prob_pass.append(prob_score)
    
    per_step_pass = sum(per_step_pass) / sum(steps_per_prob.values())
    per_prob_pass = sum(per_prob_pass) / len(steps_per_prob)

    print(f'problem-level pass@1: {per_prob_pass}')
    print(f'step-level pass@1: {per_step_pass}')

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(f'{output_dir}/{model_name}_{_get_background_dir(with_background)}.txt', 'w') as f:
        f.write(f'problem-level pass@1: {per_prob_pass}\n')
        f.write(f'step-level pass@1: {per_step_pass}\n\n')
        f.write(f'duration: {test_time} seconds\n')

    results = {
        "steps_pass@1": per_step_pass,
        "problems_pass@1": per_prob_pass,
        "n_samples": n_samples,
        "num_correct": correct_per_prob,
    }
    with open(f'{output_dir}/{model_name}_{_get_background_dir(with_background)}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    
    shutil.rmtree(tmp_dir)
    

def main(model: str,
         output_dir: Path,
         log_dir: Path,
         with_background: bool,
         temperature: float,
         url: str,
         limit_samples: Optional[int],
         n_samples: int,
         extra_params: Optional[dict],
         include_dev: bool,
         eval_threads: int,
         concurrent_requests: int,
) -> None:
    prompt_dir = output_dir / "prompt"
    code_dir = output_dir / "generated_code"
    if extra_params is None:
        extra_params = {}
    
    gcode = Gencode(
        model=model, output_dir=code_dir,
        prompt_dir=prompt_dir, with_background=with_background, temperature=temperature, url=url, **extra_params,
    )
    prompt_template = BACKGOUND_PROMPT_TEMPLATE if with_background else DEFAULT_PROMPT_TEMPLATE
    data = read_from_jsonl(INPUT_JSON_PATH)
    if include_dev:
        data += read_from_jsonl(DEV_JSON_PATH)
    if limit_samples is not None:
        data = data[:limit_samples]
        print(f"Runing evaluation on first {limit_samples} problems")

    def process_problem(gc, problem):
        prob_id = problem['problem_id']
        steps = len(problem['sub_steps'])
        print(f'Generating {prob_id}...')
        for i in range(steps):
            if (prob_id == "13" and i == 5) or (prob_id == "62" and i == 0) or (prob_id == "76" and i == 2):
                continue
            print(f'Generating {prob_id} step {i + 1}...')
            gc.generate_response_with_steps(problem, i + 1, steps, model, prompt_template, n_samples=n_samples)
        print(f'Generated {prob_id}')

    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        futures = [executor.submit(process_problem, copy.deepcopy(gcode), problem) for problem in data]
        for future in as_completed(futures):
            future.result()
    if not H5PY_FILE.exists():
        try:
            print("Downloading test data...")
            download_test_data()
        except Exception as e:
            raise FileNotFoundError(f"Test data is missing and the automatic download failed with the following error:\n\n{e}.\n\n"
                                    f"Please download the numeric test results manually and save them as {H5PY_FILE}.")
    model = Path(model).parts[-1]
    
    test_code(model, code_dir, log_dir, output_dir, data, with_background, n_samples=n_samples, eval_threads=eval_threads)

def cli_evaluate():
    args = get_cli().parse_args()
    main(**vars(args))

if __name__ == "__main__":
    cli_evaluate()
