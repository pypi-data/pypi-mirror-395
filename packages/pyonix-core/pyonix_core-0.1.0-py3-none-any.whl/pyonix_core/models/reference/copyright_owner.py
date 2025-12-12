from dataclasses import dataclass, field
from typing import Optional

from .copyright_owner_identifier import CopyrightOwnerIdentifier
from .copyright_owner_refname import CopyrightOwnerRefname
from .copyright_owner_shortname import CopyrightOwnerShortname
from .corporate_name import CorporateName
from .list3 import List3
from .person_name import PersonName

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class CopyrightOwner:
    """
    Name of and/or identifier for a copyright or neighbouring rightsholder.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    copyright_owner_identifier: list[CopyrightOwnerIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "CopyrightOwnerIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    person_name: list[PersonName] = field(
        default_factory=list,
        metadata={
            "name": "PersonName",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    corporate_name: list[CorporateName] = field(
        default_factory=list,
        metadata={
            "name": "CorporateName",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    refname: Optional[CopyrightOwnerRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CopyrightOwnerShortname] = field(
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
