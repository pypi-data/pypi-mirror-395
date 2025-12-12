from dataclasses import dataclass, field
from typing import Optional

from .event_refname import EventRefname
from .event_shortname import EventShortname
from .eventsponsor import Eventsponsor
from .list3 import List3
from .website import Website
from .x515 import X515
from .x516 import X516
from .x517 import X517
from .x518 import X518
from .x519 import X519
from .x520 import X520
from .x521 import X521

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Event:
    """
    Details of an event (eg conference, exhibition, sporting event) to which the
    product is related ● Added at revision 3.0.3.
    """

    class Meta:
        name = "event"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x515: Optional[X515] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x516: list[X516] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    x517: list[X517] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x518: Optional[X518] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x519: list[X519] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x520: Optional[X520] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x521: list[X521] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    eventsponsor: list[Eventsponsor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    website: list[Website] = field(
        default_factory=list,
        metadata={
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
