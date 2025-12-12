from dataclasses import dataclass, field
from typing import Optional

from .event_acronym import EventAcronym
from .event_date import EventDate
from .event_name import EventName
from .event_number import EventNumber
from .event_place import EventPlace
from .event_refname import EventRefname
from .event_role import EventRole
from .event_shortname import EventShortname
from .event_sponsor import EventSponsor
from .event_theme import EventTheme
from .list3 import List3
from .website import Website

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Event:
    """
    Details of an event (eg conference, exhibition, sporting event) to which the
    product is related ● Added at revision 3.0.3.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    event_role: Optional[EventRole] = field(
        default=None,
        metadata={
            "name": "EventRole",
            "type": "Element",
            "required": True,
        },
    )
    event_name: list[EventName] = field(
        default_factory=list,
        metadata={
            "name": "EventName",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    event_acronym: list[EventAcronym] = field(
        default_factory=list,
        metadata={
            "name": "EventAcronym",
            "type": "Element",
        },
    )
    event_number: Optional[EventNumber] = field(
        default=None,
        metadata={
            "name": "EventNumber",
            "type": "Element",
        },
    )
    event_theme: list[EventTheme] = field(
        default_factory=list,
        metadata={
            "name": "EventTheme",
            "type": "Element",
        },
    )
    event_date: Optional[EventDate] = field(
        default=None,
        metadata={
            "name": "EventDate",
            "type": "Element",
        },
    )
    event_place: list[EventPlace] = field(
        default_factory=list,
        metadata={
            "name": "EventPlace",
            "type": "Element",
        },
    )
    event_sponsor: list[EventSponsor] = field(
        default_factory=list,
        metadata={
            "name": "EventSponsor",
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
    refname: Optional[EventRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[EventShortname] = field(
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
