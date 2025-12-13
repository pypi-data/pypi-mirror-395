from dataclasses import dataclass, field
from typing import Optional

from .conference_acronym import ConferenceAcronym
from .conference_date import ConferenceDate
from .conference_name import ConferenceName
from .conference_number import ConferenceNumber
from .conference_place import ConferencePlace
from .conference_refname import ConferenceRefname
from .conference_role import ConferenceRole
from .conference_shortname import ConferenceShortname
from .conference_sponsor import ConferenceSponsor
from .conference_theme import ConferenceTheme
from .list3 import List3
from .website import Website

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Conference:
    """
    ● Deprecated – use &lt;Event&gt; instead.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    conference_role: Optional[ConferenceRole] = field(
        default=None,
        metadata={
            "name": "ConferenceRole",
            "type": "Element",
        },
    )
    conference_name: Optional[ConferenceName] = field(
        default=None,
        metadata={
            "name": "ConferenceName",
            "type": "Element",
            "required": True,
        },
    )
    conference_acronym: Optional[ConferenceAcronym] = field(
        default=None,
        metadata={
            "name": "ConferenceAcronym",
            "type": "Element",
        },
    )
    conference_number: Optional[ConferenceNumber] = field(
        default=None,
        metadata={
            "name": "ConferenceNumber",
            "type": "Element",
        },
    )
    conference_theme: Optional[ConferenceTheme] = field(
        default=None,
        metadata={
            "name": "ConferenceTheme",
            "type": "Element",
        },
    )
    conference_date: Optional[ConferenceDate] = field(
        default=None,
        metadata={
            "name": "ConferenceDate",
            "type": "Element",
        },
    )
    conference_place: Optional[ConferencePlace] = field(
        default=None,
        metadata={
            "name": "ConferencePlace",
            "type": "Element",
        },
    )
    conference_sponsor: list[ConferenceSponsor] = field(
        default_factory=list,
        metadata={
            "name": "ConferenceSponsor",
            "type": "Element",
        },
    )
    website: list[Website] = field(
        default_factory=list,
        metadata={
            "name": "Website",
            "type": "Element",
        },
    )
    refname: Optional[ConferenceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ConferenceShortname] = field(
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
