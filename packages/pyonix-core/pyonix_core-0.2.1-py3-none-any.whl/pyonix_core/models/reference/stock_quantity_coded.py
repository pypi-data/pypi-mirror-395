from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .stock_quantity_code import StockQuantityCode
from .stock_quantity_code_type import StockQuantityCodeType
from .stock_quantity_code_type_name import StockQuantityCodeTypeName
from .stock_quantity_coded_refname import StockQuantityCodedRefname
from .stock_quantity_coded_shortname import StockQuantityCodedShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class StockQuantityCoded:
    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    stock_quantity_code_type: Optional[StockQuantityCodeType] = field(
        default=None,
        metadata={
            "name": "StockQuantityCodeType",
            "type": "Element",
            "required": True,
        },
    )
    stock_quantity_code_type_name: Optional[StockQuantityCodeTypeName] = field(
        default=None,
        metadata={
            "name": "StockQuantityCodeTypeName",
            "type": "Element",
        },
    )
    stock_quantity_code: Optional[StockQuantityCode] = field(
        default=None,
        metadata={
            "name": "StockQuantityCode",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[StockQuantityCodedRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[StockQuantityCodedShortname] = field(
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
