"""
Copyright 2023 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

import pydantic


def regex_string(regex: str) -> type:
    """
    Build a regex constrained string that is both supported by pydantic v1 and v2

    :param regex: A regex string
    :return: A type that the current pydantic can use for validation
    """
    try:
        from inmanta.validation_type import regex_string as core_regex_string
    except ImportError:
        # v1 (all versions of core that use v2 have this method)
        return pydantic.constr(regex=regex)
    else:
        # delegate to core
        return core_regex_string(regex)
