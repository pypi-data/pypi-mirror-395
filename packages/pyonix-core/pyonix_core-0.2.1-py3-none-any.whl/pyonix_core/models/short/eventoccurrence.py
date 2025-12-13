from dataclasses import dataclass, field
from typing import Optional

from .b251 import B251
from .b398 import B398
from .eventidentifier import Eventidentifier
from .eventoccurrence_refname import EventoccurrenceRefname
from .eventoccurrence_shortname import EventoccurrenceShortname
from .eventsponsor import Eventsponsor
from .j349 import J349
from .list3 import List3
from .occurrencedate import Occurrencedate
from .supportingresource import Supportingresource
from .website import Website
from .x549 import X549
from .x550 import X550
from .x551 import X551
from .x552 import X552
from .x553 import X553

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Eventoccurrence:
    """
    Details for a particular occurrence of a promotional event ● Added
    &lt;SupportingResource&gt; at revision 3.0.8 ● Added at revision 3.0.7.
    """

    class Meta:
        name = "eventoccurrence"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    eventidentifier: list[Eventidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    occurrencedate: list[Occurrencedate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    x549: Optional[X549] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b251: Optional[B251] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b398: list[B398] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    j349: list[J349] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x551: Optional[X551] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x552: Optional[X552] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x553: list[X553] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x550: list[X550] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supportingresource: list[Supportingresource] = field(
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
    refname: Optional[EventoccurrenceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[EventoccurrenceShortname] = field(
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
