from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .percent import Percent
from .product_classification_code import ProductClassificationCode
from .product_classification_refname import ProductClassificationRefname
from .product_classification_shortname import ProductClassificationShortname
from .product_classification_type import ProductClassificationType
from .product_classification_type_name import ProductClassificationTypeName

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ProductClassification:
    """
    Details of a national or international trade classification (eg HMRC customs
    code, TARIC code, Schedule B code) ● Added
    &lt;ProductClassificationTypeName&gt; at revision 3.0.7.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    product_classification_type: Optional[ProductClassificationType] = field(
        default=None,
        metadata={
            "name": "ProductClassificationType",
            "type": "Element",
            "required": True,
        },
    )
    product_classification_type_name: Optional[
        ProductClassificationTypeName
    ] = field(
        default=None,
        metadata={
            "name": "ProductClassificationTypeName",
            "type": "Element",
        },
    )
    product_classification_code: Optional[ProductClassificationCode] = field(
        default=None,
        metadata={
            "name": "ProductClassificationCode",
            "type": "Element",
            "required": True,
        },
    )
    percent: Optional[Percent] = field(
        default=None,
        metadata={
            "name": "Percent",
            "type": "Element",
        },
    )
    refname: Optional[ProductClassificationRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductClassificationShortname] = field(
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
