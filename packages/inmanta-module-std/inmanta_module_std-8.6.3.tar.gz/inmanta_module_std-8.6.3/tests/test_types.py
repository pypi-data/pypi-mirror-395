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

import string
from typing import Union

import pytest

from inmanta.ast import AttributeException


@pytest.mark.parametrize(
    "attr_type,value,is_valid",
    [
        ("std::date", '"2019-03-04"', True),
        ("std::date", '"2019-24-04"', False),
        ("std::time", '"12:33:45"', True),
        ("std::time", '"25:33:45"', False),
        ("std::datetime", '"2019-07-31T02:03:59"', True),
        ("std::datetime", '"2019-07-31T02:03:60"', False),
        ("std::ipv4_address", '"192.168.11.33"', True),
        ("std::ipv4_address", '"192.168.11.256"', False),
        ("std::ipv4_address", '"1.1.1.1/32"', False),
        ("std::ipv4_address", '"2001:0db8:85a3:0000:0000:8a2e:0370:7334"', False),
        ("std::ipv4_interface", '"192.1.2.3/24"', True),
        ("std::ipv4_interface", '"192.1.2.3/33"', False),
        ("std::ipv4_network", '"192.1.5.0/24"', True),
        ("std::ipv4_network", '"192.1.5.1/24"', False),
        ("std::ipv6_address", '"2001:db8:85a3:8d3:1319:8a2e:370:7348"', True),
        ("std::ipv6_address", '"2001:db8:85a3:8d3:1319:8a2e:370:734z"', False),
        ("std::ipv6_address", '"192.168.5.3"', False),
        ("std::ipv6_address", '"5236"', False),
        ("std::ipv6_address", '"2001:0db8:85a3::8a2e:0370:7334"', True),
        ("std::ipv6_interface", '"2001:db8:85a3:8d3:1319:8a2e:370:7348/64"', True),
        ("std::ipv6_interface", '"2001:db8:85a3:8d3:1319:8a2e:370:7348/129"', False),
        ("std::ipv6_network", '"2001:db8:85a3:8d3::/64"', True),
        ("std::ipv6_network", '"2001:db8:85a3:8d3::1/64"', False),
        ("std::uuid", '"35ea1490-f3d4-4b1d-99e7-52c258f7848e"', True),
        ("std::uuid", '"35ea1490-f3d4-4b1d-99e7-52c258f7848"', False),
        ("std::email_str", '"test@host.com"', True),
        ("std::email_str", '"testhost.com"', False),
        ("std::name_email", '"Test user <test-user@inmanta.com>"', True),
        ("std::name_email", '"Test user <test-user@inmanta.com"', False),
        ("std::any_url", '"ssh://host.com"', True),
        ("std::any_http_url", '"http://host:8080"', True),
        ("std::any_http_url", '"ssh://host:8080"', False),
        ("std::http_url", '"http://host.com:8080"', True),
        ("std::ipv_any_address", '"192.168.2.11"', True),
        ("std::ipv_any_address", '"192.168.2.1111"', False),
        ("std::ipv_any_address", '"2z01:0db8:85a3:0000:0000:8a2e:0370:7334"', False),
        ("std::ipv_any_address", '"2001:0db8:85a3::8a2e:0370:7334"', True),
        ("std::ipv_any_address", '"2001:0db8:85a3:0000:0000:8a2e:0370:7334"', True),
        ("std::ipv_any_interface", '"fe80::1/64"', True),
        ("std::ipv_any_interface", '"fe80::g111/16"', False),
        ("std::ipv_any_network", '"1234::/16"', True),
        ("std::ipv_any_network", '"1234::1/16"', False),
        ("std::negative_float", "-1.2", True),
        ("std::negative_float", "1.2", False),
        ("std::negative_int", "-2", True),
        ("std::negative_int", "0", False),
        ("std::positive_float", "2.6", True),
        ("std::positive_float", "-2.3", False),
        ("std::positive_int", "5", True),
        ("std::positive_int", "0", False),
        ("std::alfanum", '"Qwerty123"', True),
        ("std::alfanum", '"qwerty/123"', False),
        ("std::base64", '"dGVzdA=="', True),
        ("std::base64", '"dGVzdA="', False),
        ("std::non_empty_string", '""', False),
        ("std::non_empty_string", '"a"', True),
        ("std::non_empty_string", '"a "', True),
        ("std::non_empty_string", '"  a  "', True),
        ("std::non_empty_string", '"    "', False),
    ],
)
def test_attribute_types(project, attr_type, value, is_valid):
    model = f"""
            entity Test:
                {attr_type} attr
            end

            implement Test using std::none

            Test(attr={value})
            """
    if is_valid:
        project.compile(model)
    else:
        with pytest.raises(AttributeException):
            project.compile(model)


@pytest.mark.parametrize(
    "attr_type,base_type,value,validation_parameters,is_optional,is_valid",
    [
        ("pydantic.condecimal", "number", 8, '{"gt": 0, "lt": 10}', False, True),
        ("pydantic.condecimal", "number", 8, '{"gt": 0, "lt": 5}', False, False),
        ("pydantic.confloat", "number", 1.5, '{"multiple_of": 0.5}', False, True),
        ("pydantic.confloat", "number", 1.5, '{"multiple_of": 0.2}', False, False),
        ("pydantic.conint", "number", 4, '{"ge": 4}', False, True),
        ("pydantic.conint", "number", 4, '{"ge": 5}', False, False),
        (
            "pydantic.constr",
            "string",
            '"test123"',
            '{"regex": "^test.*$"}',
            False,
            True,
        ),
        (
            "pydantic.constr",
            "string",
            '"test123"',
            '{"regex": "^tst.*$"}',
            False,
            False,
        ),
        ("pydantic.constr", "string", "null", '{"regex": "^tst.*$"}', True, True),
        ("pydantic.constr", "string", "null", '{"regex": "^tst.*$"}', False, False),
        (
            "pydantic.constr",
            "string",
            # Test for Unknown values
            "std::get_env(name='non-existing-env-var')",
            '{"regex": "^tst.*$"}',
            False,
            True,
        ),
    ],
)
def test_constrained_types(
    project,
    attr_type: str,
    base_type: str,
    value: Union[str, int],
    validation_parameters: str,
    is_optional: bool,
    is_valid: bool,
):
    model = f"""
            typedef custom_type as {base_type} matching std::validate_type("{attr_type}", self, {validation_parameters})

            entity Test:
                custom_type{"?" if is_optional else ""} attr
            end

            implement Test using std::none

            Test(attr={value})
            """
    if is_valid:
        project.compile(model)
    else:
        with pytest.raises(AttributeException):
            project.compile(model)


@pytest.mark.parametrize(
    "type_name,allow_whitespace",
    [("std::printable_ascii", True), ("std::ascii_word", False)],
)
def test_printable_ascii_type(project, type_name, allow_whitespace):
    # Test valid characters
    all_char_string = string.ascii_letters + string.digits + string.punctuation
    if allow_whitespace:
        all_char_string += " "
    char_set = set([s for s in all_char_string if s != '"' and s != "\\"])
    char_set.add('\\"')  # Escape double quote
    char_set.add("\\\\")  # Escape backslash
    for char in char_set:
        model = f"""
                    entity Test:
                        {type_name} attr
                    end

                    implement Test using std::none

                    Test(attr="{char}c")
                    """
        project.compile(model)

    # Test invalid characters
    invalid_strings = ["val1\tval2", "test\x0b", "\x0ctest"]
    if not allow_whitespace:
        invalid_strings.append("test 123")
    for s in invalid_strings:
        model = f"""
                    entity Test:
                        {type_name} attr
                    end

                    implement Test using std::none

                    Test(attr="{s}")
                    """

        with pytest.raises(AttributeException):
            project.compile(model)
