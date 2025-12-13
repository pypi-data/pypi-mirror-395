from dataclasses import dataclass, field
from typing import Optional

from .idtype_name import IdtypeName
from .idvalue import Idvalue
from .list3 import List3
from .text_item_identifier_refname import TextItemIdentifierRefname
from .text_item_identifier_shortname import TextItemIdentifierShortname
from .text_item_idtype import TextItemIdtype

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class TextItemIdentifier:
    """
    Identifier for a textual content item (eg a chapter)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    text_item_idtype: Optional[TextItemIdtype] = field(
        default=None,
        metadata={
            "name": "TextItemIDType",
            "type": "Element",
            "required": True,
        },
    )
    idtype_name: Optional[IdtypeName] = field(
        default=None,
        metadata={
            "name": "IDTypeName",
            "type": "Element",
        },
    )
    idvalue: Optional[Idvalue] = field(
        default=None,
        metadata={
            "name": "IDValue",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[TextItemIdentifierRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TextItemIdentifierShortname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    datestamp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"(19|20)\d\d(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-8])(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|(19|20)\d\d(0[13-9]|1[0-2])(29|30)(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|(19|20)\d\d(0[13578]|1[02])31(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|19(0[48]|[13579][26]|[2468][048])0229(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|20(0[048]|[13579][26]|[2468][048])0229(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?",
        },
    )
    sourcename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"\S(.*\S)?",
        },
    )
    sourcetype: Optional[List3] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
