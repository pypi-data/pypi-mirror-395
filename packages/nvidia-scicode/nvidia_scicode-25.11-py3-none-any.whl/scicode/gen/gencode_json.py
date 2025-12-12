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
# Original Copyright 2025 scicode-bench
# For the original license and copyright information, see the LICENSE file in this repository.

from importlib import resources
from pathlib import Path
from typing import Optional

from scicode.parse.parse import (
    extract_function_name,
    get_function_from_code
)
from scicode.gen.models import extract_python_script, get_model_function
DEFAULT_PROMPT_TEMPLATE = resources.read_text("scicode.data", "background_comment_template.txt")

class Gencode:
    def __init__(self, model: str, output_dir: Path,
                 prompt_dir: Path, with_background: bool, **model_kwargs):
        self.model = model
        self.output_dir = output_dir
        self.prompt_dir = prompt_dir
        self.with_background = with_background
        self.previous_llm_code = []
        self.model_kwargs = model_kwargs

    def _get_background_dir(self):
        return "with_background" if self.with_background else "without_background"

    def save_prompt_with_steps(self, prob_data: dict, prompt: str, num_steps: int) -> None:
        output_dir = Path(self.prompt_dir, Path(self.model).parts[-1], self._get_background_dir())
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file_path = output_dir / f"{prob_data['problem_id']}.{num_steps}.txt"
        output_file_path.write_text(prompt, encoding="utf-8")

    def save_response_with_steps(self, prob_data: dict, response: str,
                                 previous_code: str, num_steps: int, repeat_num: int = 1) -> None:
        output_dir = (
                self.output_dir / Path(self.model).parts[-1] / self._get_background_dir()
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        prob_id = prob_data["problem_id"]
        output_file_path = output_dir / f"{prob_id}.{num_steps}_{repeat_num}.py"
        python_code = extract_python_script(response)
        output_file_path.write_text(f'{previous_code}\n{python_code}', encoding="utf-8")

    def generate_response_with_steps(
        self, prob_data: dict, num_steps: int, tot_steps: int, model="gpt-4o",
            prompt_template=DEFAULT_PROMPT_TEMPLATE, n_samples: int = 1,
            *, save: bool = True) -> None:
        """

        Args:
            prob_data (dict): dict of the problem
            num_steps (int): Current generating step
            tot_steps (int): Total step of the problem
            model (str)
            prompt_template (str)
            n_samples (int): Number of responses to generate for the prompt
            save (bool, optional): Save propmt and model response. Defaults to True.
        """
        for repeat_num in range(n_samples):
            prob_id = prob_data["problem_id"]
            output_file_path = (
                    self.output_dir / Path(self.model).parts[-1] / self._get_background_dir()
                    / f"{prob_id}.{num_steps}_{repeat_num}.py"
            )
            if num_steps == 1:
                self.previous_llm_code = [None] * tot_steps
            else:
                if len(self.previous_llm_code) != tot_steps:
                    self.previous_llm_code = [None] * tot_steps
                for prev_step in range(num_steps - 1):
                    if self.previous_llm_code[prev_step] is None:
                        if (prob_id == "13" and prev_step == 5) or (prob_id == "62" and prev_step == 0)\
                                or (prob_id == "76" and prev_step == 2):
                            with resources.path("scicode.data", f"{prob_id}.{prev_step+1}.txt") as p:
                                prev_file_path = p
                        else:
                            prev_file_path = (
                                    self.output_dir / Path(self.model).parts[-1] / self._get_background_dir()
                                    / f"{prob_id}.{prev_step + 1}_{repeat_num}.py"
                            )
                        if prev_file_path.is_file():
                            prev_file_content = prev_file_path.read_text(encoding='utf-8')
                            func_name = extract_function_name(prob_data["sub_steps"][prev_step]["function_header"])
                            function_code = get_function_from_code(prev_file_content, func_name)
                            self.previous_llm_code[prev_step] = function_code
                        else:
                            raise Exception(f'Generating {prob_id} step {num_steps} ahead of step {prev_step + 1}.')

            if output_file_path.exists():
                return
            prompt, previous_code = self.generate_prompt_with_steps(prob_data, num_steps, prompt_template)
            if save:
                self.save_prompt_with_steps(prob_data, prompt, num_steps)

            # write the response to a file if it doesn't exist
            model_fct = get_model_function(model, **self.model_kwargs)
            response_from_llm = model_fct(prompt)
            self.previous_llm_code[num_steps - 1] = extract_python_script(response_from_llm)
            self.save_response_with_steps(prob_data, response_from_llm, previous_code, num_steps, repeat_num=repeat_num)

    @staticmethod
    def process_problem_code(prob_data: dict, num_steps: int) -> str:
        header_docstring = prob_data['sub_steps'][num_steps - 1]['function_header']
        return_str = prob_data['sub_steps'][num_steps - 1]['return_line']
        string = f"{header_docstring}\n\n{return_str}"
        return string

    def process_problem_steps(self, problem_data: dict, num_steps: int):
        """Process problem data and return previous steps and next steps"""
        output_lines = []
        next_step = []
        previous_code = []
        for i in range(num_steps - 1):
            output_lines.append(problem_data["sub_steps"][i]["step_description_prompt"] + '\n' +
                                problem_data["sub_steps"][i]["step_background"] if self.with_background
                                else problem_data["sub_steps"][i]["step_description_prompt"])
            output_lines.append(self.previous_llm_code[i])
            previous_code.append(self.previous_llm_code[i])
            output_lines.append("------")

        next_step.append(problem_data["sub_steps"][num_steps - 1]["step_description_prompt"] + '\n' +
                         problem_data["sub_steps"][num_steps - 1]["step_background"] if self.with_background
                         else problem_data["sub_steps"][num_steps - 1]["step_description_prompt"])
        next_step.append(self.process_problem_code(problem_data, num_steps))
        output_str = "\n\n".join(output_lines[:-1])  # Remove the last "------"
        next_step_str = "\n\n".join(next_step)
        previous_code_str = "\n".join(previous_code)
        return output_str, next_step_str, previous_code_str

    def generate_prompt_with_steps(self, prob_data: dict, num_steps: int,
                                   prompt_template=DEFAULT_PROMPT_TEMPLATE):
        # parse the input file and extract the content
        problem_steps_str, next_step_str, previous_code_str = self.process_problem_steps(prob_data,
                                                                                         num_steps)
        dependencies = prob_data["required_dependencies"]
        assert next_step_str
        return prompt_template.format(
            problem_steps_str=problem_steps_str,
            next_step_str=next_step_str,
            dependencies=dependencies,
        ), f'{dependencies}\n{previous_code_str}\n'
