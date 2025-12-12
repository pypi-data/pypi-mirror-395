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

import logging
from rich.logging import RichHandler

_SET_UP_LOGGERS = set()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if name in _SET_UP_LOGGERS:
        # Already set up
        return logger
    handler = RichHandler(show_time=False, show_path=False)
    handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False
    _SET_UP_LOGGERS.add(name)
    return logger


default_logger = get_logger('scicode')