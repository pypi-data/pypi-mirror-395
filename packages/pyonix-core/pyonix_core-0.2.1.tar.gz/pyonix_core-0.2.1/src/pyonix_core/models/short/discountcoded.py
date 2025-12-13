from dataclasses import dataclass, field
from typing import Optional

from .discountcoded_refname import DiscountcodedRefname
from .discountcoded_shortname import DiscountcodedShortname
from .j363 import J363
from .j364 import J364
from .j378 import J378
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Discountcoded:
    """
    Details of the trade discount offered by the supplier, in a coded manner.
    """

    class Meta:
        name = "discountcoded"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    j363: Optional[J363] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    j378: Optional[J378] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j364: Optional[J364] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[DiscountcodedRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[DiscountcodedShortname] = field(
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
