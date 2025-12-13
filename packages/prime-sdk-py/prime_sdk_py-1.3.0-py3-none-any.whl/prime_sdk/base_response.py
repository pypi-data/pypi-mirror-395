# Copyright 2024-present Coinbase Global, Inc.
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

import json
import dataclasses
from dataclasses import dataclass, fields, asdict
from typing import get_type_hints

@dataclass
class BaseResponse:
    def __post_init__(self):
        type_hints = get_type_hints(self.__class__)
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            expected_type = type_hints.get(f.name)
            if hasattr(expected_type, '__origin__') and expected_type.__origin__ is list:
                inner_type = expected_type.__args__[0]
                if dataclasses.is_dataclass(inner_type) and isinstance(value, list):
                    setattr(self, f.name, [inner_type(**v) if isinstance(v, dict) else v for v in value])
            elif dataclasses.is_dataclass(expected_type) and isinstance(value, dict):
                setattr(self, f.name, expected_type(**value))

    def __str__(self):
        return json.dumps(asdict(self), indent=2)

    def __repr__(self):
        return self.__str__()