from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .pricecoded_refname import PricecodedRefname
from .pricecoded_shortname import PricecodedShortname
from .x465 import X465
from .x468 import X468
from .x477 import X477

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Pricecoded:
    """
    Details of a coded price applied to a product (ie a price not in a specific
    currency) ● Added at revision 3.0 (2010)
    """

    class Meta:
        name = "pricecoded"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x465: Optional[X465] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x477: Optional[X477] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x468: Optional[X468] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[PricecodedRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PricecodedShortname] = field(
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
