"""
Copyright 2019 Inmanta

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

import pytest


def test_is_unknown_should_be_false(project):
    project.compile(
        """
    value = "value"
    std::print(std::is_unknown(value))
    """
    )

    assert project.get_stdout() == "False\n"


def test_is_unknown_should_be_true(project):
    project.compile(
        """
    unknown_env_int = std::get_env_int("UNKNOWN_ENV_INT")
    std::print(std::is_unknown(unknown_env_int))
    """
    )

    assert project.get_stdout() == "True\n"


def test_unknown_environment(project):
    """
    Ensure that an exception is raised when the std::environment() plugin is called when no environment is configured.
    """
    with pytest.raises(Exception):
        project.compile(
            """
        env_name = std::environment()
        """
        )
