from dataclasses import dataclass, field
from typing import Optional

from .event_identifier_refname import EventIdentifierRefname
from .event_identifier_shortname import EventIdentifierShortname
from .event_idtype import EventIdtype
from .idtype_name import IdtypeName
from .idvalue import Idvalue
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class EventIdentifier:
    """
    Identifier for an event ● Added at revision 3.0.7.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    event_idtype: Optional[EventIdtype] = field(
        default=None,
        metadata={
            "name": "EventIDType",
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
    refname: Optional[EventIdentifierRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[EventIdentifierShortname] = field(
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
