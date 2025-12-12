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

import requests
from typing import Optional

from scicode.parse.parse import H5PY_FILE

FILE_ID = "17G_k65N_6yFFZ2O-jQH00Lh6iaw3z-AW"
DATA_URL = f"https://drive.usercontent.google.com/download?id={FILE_ID}&confirm=y"


def download_file(url: str, target_filepath: Optional[str] = None) -> str:
    if target_filepath is None:
        target_filepath = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(target_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return target_filepath

def download_test_data():
    download_file(DATA_URL, H5PY_FILE)
