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

from inmanta.module import Project


def test_agent_config(project: Project):
    project.compile(
        """
        import std

        host = std::Host(
            name="test",
            ip="127.0.0.1",
            os=std::linux,
        )
    """
    )
    agent_config = project.get_resource("std::AgentConfig")
    assert not agent_config

    project.compile(
        """
        import std

        host = std::Host(
            name="test",
            ip="127.0.0.1",
            os=std::linux,
            remote_agent=true,
        )
    """
    )

    agent_config = project.get_resource("std::AgentConfig")
    assert agent_config
    assert agent_config.uri == "ssh://root@127.0.0.1:22?python=python"

    project.compile(
        """
        import std

        host = std::Host(
            name="test",
            ip="127.0.0.1",
            os=std::OS(name="testos", family=std::unix, python_cmd="test"),
            remote_agent=true,
        )
    """
    )

    agent_config = project.get_resource("std::AgentConfig")
    assert agent_config
    assert agent_config.uri == "ssh://root@127.0.0.1:22?python=test"
