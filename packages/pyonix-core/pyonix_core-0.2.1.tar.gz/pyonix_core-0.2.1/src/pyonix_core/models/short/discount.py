from dataclasses import dataclass, field
from typing import Optional

from .discount_refname import DiscountRefname
from .discount_shortname import DiscountShortname
from .j267 import J267
from .list3 import List3
from .x320 import X320
from .x467 import X467
from .x469 import X469
from .x514 import X514

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Discount:
    """
    Details of the trade discount offered by the supplier, as a percentage of the
    price or an absolute amount per copy ● Added &lt;ToQuantity&gt; at revison
    3.0.2.
    """

    class Meta:
        name = "discount"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x467: Optional[X467] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x320: Optional[X320] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x514: Optional[X514] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j267: Optional[J267] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x469: list[X469] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    refname: Optional[DiscountRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[DiscountShortname] = field(
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
