from dataclasses import dataclass, field
from typing import Optional

from .conference_sponsor_identifier import ConferenceSponsorIdentifier
from .conference_sponsor_refname import ConferenceSponsorRefname
from .conference_sponsor_shortname import ConferenceSponsorShortname
from .corporate_name import CorporateName
from .list3 import List3
from .person_name import PersonName

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ConferenceSponsor:
    """
    ● Deprecated – use &lt;EventSponsor&gt; instead.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    conference_sponsor_identifier: list[ConferenceSponsorIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ConferenceSponsorIdentifier",
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
    refname: Optional[ConferenceSponsorRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ConferenceSponsorShortname] = field(
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
