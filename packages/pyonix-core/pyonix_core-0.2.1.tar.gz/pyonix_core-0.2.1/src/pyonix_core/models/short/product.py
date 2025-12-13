from dataclasses import dataclass, field
from typing import Optional

from .a001 import A001
from .a002 import A002
from .a194 import A194
from .a197 import A197
from .a199 import A199
from .barcode import Barcode
from .collateraldetail import Collateraldetail
from .contentdetail import Contentdetail
from .descriptivedetail import Descriptivedetail
from .list3 import List3
from .product_refname import ProductRefname
from .product_shortname import ProductShortname
from .productidentifier import Productidentifier
from .productiondetail import Productiondetail
from .productsupply import Productsupply
from .promotiondetail import Promotiondetail
from .publishingdetail import Publishingdetail
from .recordsourceidentifier import Recordsourceidentifier
from .relatedmaterial import Relatedmaterial

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Product:
    """
    Container for details of a single product ● Added &lt;ProductionDetail&gt;
    (Block 8) at revision 3.0.8 ● Added &lt;PromotionDetail&gt; (Block 7) at
    revision 3.0.7 ● Modified cardinality of &lt;DeletionText&gt; at revision
    3.0.1.
    """

    class Meta:
        name = "product"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    a001: Optional[A001] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    a002: Optional[A002] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    a199: list[A199] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    a194: Optional[A194] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    recordsourceidentifier: list[Recordsourceidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    a197: Optional[A197] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    productidentifier: list[Productidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    barcode: list[Barcode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    descriptivedetail: Optional[Descriptivedetail] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    collateraldetail: Optional[Collateraldetail] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    promotiondetail: Optional[Promotiondetail] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    contentdetail: Optional[Contentdetail] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    publishingdetail: Optional[Publishingdetail] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    relatedmaterial: Optional[Relatedmaterial] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    productiondetail: Optional[Productiondetail] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    productsupply: list[Productsupply] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ProductRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductShortname] = field(
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
