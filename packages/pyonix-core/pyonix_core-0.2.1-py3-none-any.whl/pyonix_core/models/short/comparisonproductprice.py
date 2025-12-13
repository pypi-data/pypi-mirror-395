from dataclasses import dataclass, field
from typing import Optional

from .comparisonproductprice_refname import ComparisonproductpriceRefname
from .comparisonproductprice_shortname import ComparisonproductpriceShortname
from .j151 import J151
from .j152 import J152
from .list3 import List3
from .productidentifier import Productidentifier
from .x462 import X462

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Comparisonproductprice:
    """
    ● Added at revision 3.0 (2010)
    """

    class Meta:
        name = "comparisonproductprice"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    productidentifier: list[Productidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    x462: Optional[X462] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j151: Optional[J151] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    j152: Optional[J152] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ComparisonproductpriceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ComparisonproductpriceShortname] = field(
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
