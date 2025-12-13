from dataclasses import dataclass, field
from typing import Optional

from .idtype_name import IdtypeName
from .idvalue import Idvalue
from .list3 import List3
from .name_identifier_refname import NameIdentifierRefname
from .name_identifier_shortname import NameIdentifierShortname
from .name_idtype import NameIdtype

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class NameIdentifier:
    """
    Identifier for the name of a person, persona or corporate identity, eg for the
    name of a contributor, or a name as subject.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    name_idtype: Optional[NameIdtype] = field(
        default=None,
        metadata={
            "name": "NameIDType",
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
    refname: Optional[NameIdentifierRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[NameIdentifierShortname] = field(
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
