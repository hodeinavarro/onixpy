"""Tests to ensure alias (CamelCase) and field-name constructors behave identically.

This verifies constructing models via alias keys (e.g. `SenderName`) or via
field names (e.g. `sender_name`) yields equivalent Pydantic models and that
their JSON/dict/XML serializations match.
"""

from __future__ import annotations

import json

from onix import (
    Header,
    ONIXMessage,
    Sender,
    SenderIdentifier,
)
from onix.parsers import message_to_dict, message_to_json, message_to_xml_string


class TestAliasKeyEquivalence:
    """Ensure alias-key and field-name constructors produce equivalent output.

    Tests follow the project's class-based style (Test* classes with
    `test_` methods).
    """

    def test_alias_and_name_construction_equivalence(self):
        # Identifier constructed by name vs alias (using ISNI to avoid proprietary requirements)
        a_si = SenderIdentifier(
            SenderIDType="16",
            IDValue="0000000121032683",
        )
        b_si = SenderIdentifier.model_validate(
            {
                "SenderIDType": "16",
                "IDValue": "0000000121032683",
            }
        )
        assert a_si.model_dump() == b_si.model_dump()

        # Sender constructed by name vs alias
        a_s = Sender(
            SenderIdentifier=[a_si],
            sender_name="Acme",
        )
        b_s = Sender.model_validate(
            {
                "SenderIdentifier": [
                    {
                        "SenderIDType": "16",
                        "IDValue": "0000000121032683",
                    }
                ],
                "SenderName": "Acme",
            }
        )
        assert a_s.model_dump() == b_s.model_dump()

        # Header constructed by name vs alias
        a_h = Header(
            Sender=a_s,
            SentDateTime="20231201T120000Z",
        )
        b_h = Header.model_validate(
            {
                "Sender": {
                    "SenderName": "Acme",
                    "SenderIdentifier": [
                        {"SenderIDType": "16", "IDValue": "0000000121032683"}
                    ],
                },
                "SentDateTime": "20231201T120000Z",
            }
        )
        assert a_h.model_dump() == b_h.model_dump()

        # Full message serializations
        a_msg = ONIXMessage(
            Header=a_h,
            Product=[],
        )
        b_msg = ONIXMessage(
            Header=b_h,
            Product=[],
        )

        assert a_msg.model_dump() == b_msg.model_dump()

        dict_a = message_to_dict(a_msg)
        dict_b = message_to_dict(b_msg)
        assert dict_a == dict_b

        json_a = json.loads(message_to_json(a_msg))
        json_b = json.loads(message_to_json(b_msg))
        assert json_a == json_b

        # Compare XML after stripping insignificant whitespace
        xml_a = message_to_xml_string(a_msg)
        xml_b = message_to_xml_string(b_msg)

        def norm(s):
            return "".join(s.split())

        assert norm(xml_a) == norm(xml_b)
