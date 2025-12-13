from dataclasses import dataclass, field
from typing import Optional

from .discount_code import DiscountCode
from .discount_code_type import DiscountCodeType
from .discount_code_type_name import DiscountCodeTypeName
from .discount_coded_refname import DiscountCodedRefname
from .discount_coded_shortname import DiscountCodedShortname
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class DiscountCoded:
    """
    Details of the trade discount offered by the supplier, in a coded manner.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    discount_code_type: Optional[DiscountCodeType] = field(
        default=None,
        metadata={
            "name": "DiscountCodeType",
            "type": "Element",
            "required": True,
        },
    )
    discount_code_type_name: Optional[DiscountCodeTypeName] = field(
        default=None,
        metadata={
            "name": "DiscountCodeTypeName",
            "type": "Element",
        },
    )
    discount_code: Optional[DiscountCode] = field(
        default=None,
        metadata={
            "name": "DiscountCode",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[DiscountCodedRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[DiscountCodedShortname] = field(
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
