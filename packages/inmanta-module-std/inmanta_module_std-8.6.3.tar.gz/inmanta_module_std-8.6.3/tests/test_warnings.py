"""
Copyright 2020 Inmanta

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

import logging

import pytest


def log_does_not_contain(caplog, loggerpart, level, msg):
    for record in caplog.get_records("call"):
        logger_name, log_level, message = record.name, record.levelno, record.message
        if msg in message and loggerpart in logger_name and level == log_level:
            return False
    return True


@pytest.mark.parametrize(
    "plugin_call,config_option",
    [
        ("std::server_token()", "compiler_rest_transport.token"),
        ("std::server_ca()", "compiler_rest_transport.ssl-ca-cert-file"),
    ],
)
def test_no_warnings(project, caplog, plugin_call, config_option):
    with caplog.at_level(logging.DEBUG):
        project.compile(
            f"""
            std::print({plugin_call})
        """
        )
    assert log_does_not_contain(
        caplog,
        "inmanta.config",
        logging.WARNING,
        f"Inconsistent default value for option {config_option}: defined as None, got",
    )

    assert project.get_stdout() == "\n"
