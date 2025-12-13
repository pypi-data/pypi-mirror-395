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

from inmanta.export import DynamicProxy


def test_mutable_string(project):
    model = """
    attr_a = std::MutableString()
    if true:
        attr_a.value = "a"
    else:
        attr_a.value = "b"
    end

    a = attr_a.value
    """

    project.compile(model)
    root = project._root_scope.get_child("__config__")
    a = root.lookup("a")
    assert a.value == "a"


def test_mutable_int(project):
    model = """
    attr_a = std::MutableInt()
    if true:
        attr_a.value = 3
    else:
        attr_a.value = 4
    end

    a = attr_a.value
    """

    project.compile(model)
    root = project._root_scope.get_child("__config__")
    a = root.lookup("a")
    assert a.value == 3


def test_mutable_float(project):
    model = """
    attr_a = std::MutableFloat()
    if true:
        attr_a.value = 8.0
    else:
        attr_a.value = 9.0
    end

    a = attr_a.value
    """

    project.compile(model)
    root = project._root_scope.get_child("__config__")
    a = root.lookup("a")
    assert a.value == 8.0


def test_mutable_bool(project):
    model = """
    attr_a = std::MutableBool()
    if true:
        attr_a.value = null
    else:
        attr_a.value = true
    end

    a = attr_a.value
    """

    project.compile(model)
    root = project._root_scope.get_child("__config__")
    a = root.lookup("a")
    assert DynamicProxy.return_value(a.value) is None
