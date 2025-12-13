from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .reviewrating_refname import ReviewratingRefname
from .reviewrating_shortname import ReviewratingShortname
from .x525 import X525
from .x526 import X526
from .x527 import X527

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Reviewrating:
    """
    Details of a ‘star rating’ awarded as part of a review of the product ● Added
    at revision 3.0.3.
    """

    class Meta:
        name = "reviewrating"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x525: Optional[X525] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x526: Optional[X526] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x527: list[X527] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ReviewratingRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ReviewratingShortname] = field(
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
