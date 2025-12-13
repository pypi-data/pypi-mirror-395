from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .price_code import PriceCode
from .price_code_type import PriceCodeType
from .price_code_type_name import PriceCodeTypeName
from .price_coded_refname import PriceCodedRefname
from .price_coded_shortname import PriceCodedShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class PriceCoded:
    """
    Details of a coded price applied to a product (ie a price not in a specific
    currency) ● Added at revision 3.0 (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    price_code_type: Optional[PriceCodeType] = field(
        default=None,
        metadata={
            "name": "PriceCodeType",
            "type": "Element",
            "required": True,
        },
    )
    price_code_type_name: Optional[PriceCodeTypeName] = field(
        default=None,
        metadata={
            "name": "PriceCodeTypeName",
            "type": "Element",
        },
    )
    price_code: Optional[PriceCode] = field(
        default=None,
        metadata={
            "name": "PriceCode",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[PriceCodedRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PriceCodedShortname] = field(
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
