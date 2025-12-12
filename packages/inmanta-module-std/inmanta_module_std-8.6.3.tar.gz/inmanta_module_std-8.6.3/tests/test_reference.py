"""
Copyright 2025 Inmanta

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

import contextlib
import re
from collections.abc import Iterator
from typing import Optional

import pytest
from pytest_inmanta.plugin import Project

from inmanta import ast, const

try:
    from inmanta.references import Reference, reference  # noqa: F401
except ImportError:
    pytestmark = pytest.skip(
        "Reference are not yet supported by this core version", allow_module_level=True
    )


# modified from inmanta-core/tests/test_references.py
@contextlib.contextmanager
def raises_wrapped(
    exc_tp: type[ast.RuntimeException], *, match: Optional[str] = None
) -> Iterator[None]:
    """
    Context manager wrapper around pytest.raises. Expects a WrappingRuntimeException to be raised, and asserts that it wraps
    the provided exception type and that its message matches the provided pattern.
    """
    with pytest.raises(ast.WrappingRuntimeException) as exc_info:
        yield
    assert isinstance(exc_info.value.__cause__, exc_tp)
    if match is not None:
        msg: str = exc_info.value.__cause__.format()
        assert re.search(match, msg) is not None, msg


def test_references_resource(project: Project, monkeypatch) -> None:

    project.compile(
        """
            import std::testing
            metavalue = std::create_environment_reference("METATESTENV")
            value = std::create_environment_reference(metavalue)
            std::testing::NullResource(agentname="test", name="aaa", value=value)

            # Test that identical references are the same value for the compiler
            value = std::create_environment_reference(metavalue)
        """
    )

    project.deploy_resource_v2(
        "std::testing::NullResource",
        name="aaa",
        expected_status=const.ResourceState.failed,
    )

    monkeypatch.setenv("METATESTENV", "TESTENV")
    monkeypatch.setenv("TESTENV", "testvalue")

    project.compile(
        """
            import std::testing
            metavalue = std::create_environment_reference("METATESTENV")
            value = std::create_environment_reference(metavalue)
            std::testing::NullResource(agentname="test", name="aaa", value=value)
        """
    )

    result = project.deploy_resource_v2("std::testing::NullResource", name="aaa")
    assert result.assert_has_logline("Observed value: testvalue")


def test_int_reference(project: Project, monkeypatch) -> None:

    project.compile(
        """
            import std
            import std::testing

            str_value = std::create_environment_reference("ENV_VALUE")
            value = std::create_int_reference(str_value)
            std::testing::NullResource(agentname="test", name="abc", int_value=value)

        """
    )
    monkeypatch.setenv("ENV_VALUE", "42")

    result = project.deploy_resource_v2("std::testing::NullResource", name="abc")
    assert result.assert_has_logline("Observed int value: 42")


def test_fact_references(project: Project) -> None:

    model = """
            import unittest
            import std::testing
            resource_a = std::testing::NullResource(agentname="test", name="aaa", value="aaa")

            resource_b = std::testing::NullResource(
                agentname="test",
                name="bbb",
                value=std::create_fact_reference(
                    resource=resource_a,
                    fact_name="my_fact",
                )
            )
        """
    project.compile(model)

    project.deploy_resource_v2(
        "std::testing::NullResource",
        name="aaa",
        expected_status=const.ResourceState.deployed,
    )

    # The aaa resource doesn't have a fact "my_fact" => fail
    project.deploy_resource_v2(
        "std::testing::NullResource",
        name="bbb",
        expected_status=const.ResourceState.failed,
    )

    # We set the fact "my_fact" to the aaa resource
    a_resource = project.get_resource("std::testing::NullResource", name="aaa")
    project.add_fact(a_resource.id, "my_fact", value="my_value")
    project.compile(model)

    # Now the reference can be resolved
    result = project.deploy_resource_v2(
        "std::testing::NullResource",
        name="bbb",
        expected_status=const.ResourceState.deployed,
    )
    assert result.assert_has_logline("Observed value: my_value")


def test_references_in_plugins(project: Project) -> None:
    """
    Verify that plugins that allow references work as expected. Does not verify results since those should be tested by
    specific implementation tests. Only verifies that no validation errors are raised.
    """
    project.compile(
        """\
        ref = std::create_environment_reference("HELLO")

        entity A:
            string s
        end
        implement A using std::none


        std::print(ref)
        std::at([ref], 0)
        std::attr(A(s=ref), "s")
        std::count([ref])
        std::len([ref])
        std::getattr(A(s=ref), "s")
        std::getattr(A(s="Hello World!"), "doesnotexist", default_value=ref)
        std::is_unknown(ref)
        """
    )


def test_references_in_jinja(project: Project) -> None:
    """
    Verify behavior of Jinja template when it encounters reference values.
    """
    project.add_mock_file(
        "templates",
        "testtemplate.j2",
        "Hello {{ world }}",
    )

    with pytest.raises(
        ast.ExplicitPluginException,
        match="Encountered reference in Jinja template for variable world",
    ):
        project.compile(
            """\
            import unittest

            world = std::create_environment_reference("WORLD")

            std::template("unittest/testtemplate.j2")
            """
        )

    project.add_mock_file(
        "templates",
        "testtemplate.j2",
        "Hello {{ world.name }}",
    )
    with raises_wrapped(
        ast.UnexpectedReference,
        match="Encountered unexpected reference .* Encountered at world.name",
    ):
        project.compile(
            """\
            import unittest

            entity World:
                string name
            end
            implement World using std::none

            world = World(name=std::create_environment_reference("WORLD"))

            std::template("unittest/testtemplate.j2")
            """
        )

    project.add_mock_file(
        "templates",
        "testtemplate.j2",
        "Hello {{ world[0].name }}",
    )
    with raises_wrapped(
        ast.UnexpectedReference,
        match=r"Encountered unexpected reference .* Encountered at world\[0\].name",
    ):
        project.compile(
            """\
            import unittest

            entity World:
                string name
            end
            implement World using std::none

            world = [World(name=std::create_environment_reference("WORLD"))]

            std::template("unittest/testtemplate.j2")
            """
        )
