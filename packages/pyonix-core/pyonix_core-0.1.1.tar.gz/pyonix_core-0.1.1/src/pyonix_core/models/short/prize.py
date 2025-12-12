from dataclasses import dataclass, field
from typing import Optional

from .g126 import G126
from .g127 import G127
from .g128 import G128
from .g129 import G129
from .g343 import G343
from .list3 import List3
from .prize_refname import PrizeRefname
from .prize_shortname import PrizeShortname
from .x503 import X503
from .x556 import X556

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Prize:
    """
    Details of a literary or other prize associated with the product or work, or
    with a contributor ● Added &lt;PrizeRegion&gt; at revision 3.0.7 ● Added
    &lt;PrizeStatement&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;PrizeName&gt; at revision 3.0.2 ● Modified cardinality of &lt;PrizeJury&gt;
    at revision 3.0.1.
    """

    class Meta:
        name = "prize"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    g126: list[G126] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    g127: Optional[G127] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    g128: Optional[G128] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x556: Optional[X556] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    g129: Optional[G129] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x503: list[X503] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    g343: list[G343] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[PrizeRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PrizeShortname] = field(
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
