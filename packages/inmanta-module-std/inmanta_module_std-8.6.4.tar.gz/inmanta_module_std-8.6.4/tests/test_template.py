"""
Copyright 2017 Inmanta

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

import os
import shutil
from typing import Dict

import pytest
import pytest_inmanta.plugin

from inmanta import ast


def test_is_defined(project):
    """
    Test the use of is defined
    """
    project.add_mock_file(
        "templates",
        "testtemplate.tmpl",
        "{% if other is defined %} {{name}} : {{ other.name }} "
        "{% if other.other is defined %} sub: {{ other.other.name }} {% endif %} "
        "{% else %} {{name}} is not defined {% endif %}"
        "",
    )

    project.compile(
        """
import std
import unittest

entity Test1:
string name
end

Test1.other [0:1] -- Test1.prev [0:1]

implementation tt for Test1:
content=std::template("unittest/testtemplate.tmpl")
std::print(content)
end

implement Test1 using tt when not(self.prev is defined)
implement Test1 using std::none when self.prev is defined

Test1(name="t1",other=Test1(name="t11"))
Test1(name="t2")
Test1(name="t3",other=Test1(name="t31",other=Test1(name="t32")))
    """
    )

    assert "t3 : t31  sub: t32" in project.get_stdout()
    assert "t1 : t11" in project.get_stdout()
    assert "t2 is not defined" in project.get_stdout()


def test_template(project: pytest_inmanta.plugin.Project) -> None:
    """
    Test the evaluation of a template
    """
    # Check that a local variable can be accessed in the template
    project.add_mock_file("templates", "test.tmpl", "{{ value }}")
    project.compile(
        """import unittest
value = "1234"
std::print(std::template("unittest/test.tmpl"))
    """
    )

    assert project.get_stdout() == "1234\n"

    # Check that an value can be passed directly to the plugin
    project.compile(
        """import unittest
std::print(std::template("unittest/test.tmpl", value="1234"))
    """
    )

    assert project.get_stdout() == "1234\n"

    # Check precedence when the value is provided by both the
    # local variable and the plugin parameter
    project.compile(
        """import unittest
value = "1234"
std::print(std::template("unittest/test.tmpl", value="5678"))
    """
    )

    assert project.get_stdout() == "5678\n"

    # Check that when we provide the wrong value, the value from the
    # model is not fetched instead
    with pytest.raises(ast.WrappingRuntimeException) as exc:
        project.compile(
            """import unittest
value = "1234"
std::print(std::template("unittest/test.tmpl", wrong_value="5678"))
        """
        )

    assert isinstance(exc.value.get_causes()[0], ast.NotFoundException), str(
        exc.value.get_causes()
    )


def test_plugin_with_list(project):
    """
    Test the use of is defined
    """
    project.add_mock_file(
        "templates",
        "test.tmpl",
        """{% for item in items | std.key_sort("name") %}  {{ item.name }}
{% endfor %}""",
    )

    project.compile(
        """
import std
import unittest

entity Item:
    string name
end

implement Item using std::none

entity Collection:
    string content
end

implementation makeContent for Collection:
    self.content = std::template("unittest/test.tmpl")
end

implement Collection using makeContent

Collection.items [0:] -- Item.collection [0:]

c1 = Collection()

t1 = Item(name="t1", collection=c1)
t2 = Item(name="t2", collection=c1)
t3 = Item(name="t3", collection=c1)
    """
    )


@pytest.fixture()
def cleanup_test_module(project):
    yield
    test_module_path = os.path.join(project._test_project_dir, "libs", "testmod")
    if os.path.exists(test_module_path):
        shutil.rmtree(test_module_path)


def test_template_current_dir(project, cleanup_test_module):
    """
    Test the use of current dir in templates
    """
    module_init_cf = """
        import std

        entity Test1:
        string name
        end

        implementation tt for Test1:
        content=std::template("./testtemplate.tmpl")
        std::print(content)
        end

        implement Test1 using tt

        Test1(name="t1")
        """
    project.create_module("testmod", initcf=module_init_cf, initpy="")
    template_dir = os.path.join(
        project._test_project_dir, "libs", "testmod", "templates"
    )
    with open(os.path.join(template_dir, "testtemplate.tmpl"), "w") as template_file:
        template_file.write("""{{name}}""")

    project.compile(
        """
import testmod
        """
    )

    assert project.get_stdout() == "t1\n"


def test_files_current_dir(project, cleanup_test_module):
    module_init_cf = """
            import std

            for file in std::list_files("./"):
                    std::source("./{{file}}")
                    std::print(file)
                end
            """

    project.create_module("testmod", initcf=module_init_cf, initpy="")
    files_dir = os.path.join(project._test_project_dir, "libs", "testmod", "files")
    with open(os.path.join(files_dir, "testfile1"), "w") as template_file:
        template_file.write("test test test")
    project.compile(
        """
        import testmod
        """
    )

    out = project.get_stdout().splitlines()
    assert ["testfile1"] == out


def test_97_template_dict_null(project):
    """
    Use a dict with null
    """
    project.add_mock_file(
        "templates",
        "test.j2",
        """
{{ value.get("test") }}
        """,
    )

    project.compile(
        """
import unittest
value = {"test": null}
std::print(std::template("unittest/test.j2"))
        """
    )

    assert "None\n" in project.get_stdout()


def test_20_template_dict_items(project):
    """
    Iterate over and get dict values from template.
    """
    project.add_mock_file(
        "templates",
        "test.j2",
        """
key-value pairs 1:
{% for key in mydict -%}
    {{ key }}: {{ mydict[key] }}
{% endfor %}

key-value pairs 2:
{% for key in mydict -%}
    {{ key }}: {{ mydict.get(key) }}
{% endfor %}

key-value-pairs 3
{% for key, value in mydict.items() -%}
    {{ key }}: {{ value }}
{% endfor %}
        """,
    )

    mydict: Dict[str, int] = {"x": 42, "y": 43, "z": 44}
    project.compile(
        f"""
import unittest

mydict = {mydict}
std::print(std::template("unittest/test.j2"))
        """
    )

    expected_out: str = """
key-value pairs 1:
x: 42
y: 43
z: 44


key-value pairs 2:
x: 42
y: 43
z: 44


key-value-pairs 3
x: 42
y: 43
z: 44
    """
    assert expected_out.strip() in project.get_stdout()


def test_218_template_dict_len(project):
    project.add_mock_file("templates", "test.j2", "{{ mydict | length }}")

    mydict: Dict[str, int] = {"x": 42, "y": 43, "z": 44}
    project.compile(
        f"""
import unittest

mydict = {mydict}
std::print(std::template("unittest/test.j2"))
        """
    )

    assert project.get_stdout().strip() == str(len(mydict))


def test_pass_undefined_to_plugin(project):
    project.add_mock_file("templates", "test.j2", "{{ myvar | std.get_env }}")

    with pytest.raises(ast.WrappingRuntimeException) as exc_info:
        project.compile(
            """
    import unittest

    std::print(std::template("unittest/test.j2"))
            """
        )
    exception_causes = exc_info.value.get_causes()
    assert len(exception_causes) == 1
    assert isinstance(exception_causes[0], ast.NotFoundException)


def test_if_defined_with_plugin_call(project):
    project.add_mock_file(
        "templates",
        "test.j2",
        "{% if myvar is defined %} {{ myvar | std.capitalize }} "
        "{% else %} myvar is not defined {% endif %}",
    )

    project.compile(
        """
    import unittest

    std::print(std::template("unittest/test.j2"))
            """
    )
    assert "myvar is not defined" in project.get_stdout()


def test_plugin_in_template_without_args(project):
    project.add_mock_file("templates", "test.j2", "{{ none | std.timestamp }}")

    project.compile(
        """
    import unittest

    std::print(std::template("unittest/test.j2"))
            """
    )
    assert project.get_stdout().strip()
