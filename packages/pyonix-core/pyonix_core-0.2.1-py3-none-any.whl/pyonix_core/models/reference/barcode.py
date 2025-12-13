from dataclasses import dataclass, field
from typing import Optional

from .barcode_refname import BarcodeRefname
from .barcode_shortname import BarcodeShortname
from .barcode_type import BarcodeType
from .list3 import List3
from .position_on_product import PositionOnProduct

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Barcode:
    """
    Details of a barcode symbology and position.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    barcode_type: Optional[BarcodeType] = field(
        default=None,
        metadata={
            "name": "BarcodeType",
            "type": "Element",
            "required": True,
        },
    )
    position_on_product: Optional[PositionOnProduct] = field(
        default=None,
        metadata={
            "name": "PositionOnProduct",
            "type": "Element",
        },
    )
    refname: Optional[BarcodeRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[BarcodeShortname] = field(
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
