from dataclasses import dataclass, field
from typing import Optional

from .b049 import B049
from .contributor import Contributor
from .contributorreference import Contributorreference
from .eventidentifier import Eventidentifier
from .eventoccurrence import Eventoccurrence
from .eventsponsor import Eventsponsor
from .list3 import List3
from .n339 import N339
from .promotionalevent_refname import PromotionaleventRefname
from .promotionalevent_shortname import PromotionaleventShortname
from .supportingresource import Supportingresource
from .website import Website
from .x427 import X427
from .x516 import X516
from .x548 import X548
from .x549 import X549
from .x550 import X550

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Promotionalevent:
    """
    Details of an event held to promote the product ● Added
    &lt;SupportingResource&gt; at revision 3.0.8 ● Added at revision 3.0.7.
    """

    class Meta:
        name = "promotionalevent"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    eventidentifier: list[Eventidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x548: list[X548] = field(
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
        },
    )
    x427: list[X427] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    x516: list[X516] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    contributorreference: list[Contributorreference] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    contributor: list[Contributor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequence": 1,
        },
    )
    b049: list[B049] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    n339: Optional[N339] = field(
        default=None,
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
    eventoccurrence: list[Eventoccurrence] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
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
    refname: Optional[PromotionaleventRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PromotionaleventShortname] = field(
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
