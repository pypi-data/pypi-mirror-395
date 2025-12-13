from dataclasses import dataclass, field
from typing import Optional

from .contributor_reference_refname import ContributorReferenceRefname
from .contributor_reference_shortname import ContributorReferenceShortname
from .contributor_role import ContributorRole
from .list3 import List3
from .name_identifier import NameIdentifier
from .sequence_number import SequenceNumber

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ContributorReference:
    """
    Reference to a contributor participating in a promotional event ● Added at
    revision 3.0.7.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sequence_number: Optional[SequenceNumber] = field(
        default=None,
        metadata={
            "name": "SequenceNumber",
            "type": "Element",
        },
    )
    contributor_role: list[ContributorRole] = field(
        default_factory=list,
        metadata={
            "name": "ContributorRole",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    name_identifier: list[NameIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "NameIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[ContributorReferenceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ContributorReferenceShortname] = field(
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
