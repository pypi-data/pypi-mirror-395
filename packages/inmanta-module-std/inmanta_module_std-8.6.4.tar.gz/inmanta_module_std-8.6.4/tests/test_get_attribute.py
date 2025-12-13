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


def test_get_attribute(project):
    project.compile(
        """
    entity Item:
        string name
    end
    implement Item using std::none
    item1 = Item(name="ItemName")
    std::print(std::getattr(item1, 'name'))
    """
    )

    assert project.get_stdout() == "ItemName\n"


def test_getattr_default_value(project):
    project.compile(
        """
    entity Item:
        string name
    end
    implement Item using std::none
    item1 = Item(name="Name")
    std::print(std::getattr(item1, 'id', 'id1'))
        """
    )

    assert project.get_stdout() == "id1\n"


def test_getattr_no_default(project):
    project.compile(
        """
    entity Item:
        string name
    end
    implement Item using std::none
    item1 = Item(name="Name")
    std::print(std::getattr(item1, 'id'))
        """
    )

    assert project.get_stdout() == "None\n"
