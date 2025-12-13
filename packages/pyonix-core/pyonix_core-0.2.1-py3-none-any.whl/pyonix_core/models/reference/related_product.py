from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .product_form import ProductForm
from .product_form_detail import ProductFormDetail
from .product_identifier import ProductIdentifier
from .product_relation_code import ProductRelationCode
from .related_product_refname import RelatedProductRefname
from .related_product_shortname import RelatedProductShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class RelatedProduct:
    """
    Details of another product related in some way to the product ● Added
    &lt;ProductForm&gt;, &lt;ProductFormDetail&gt; at revision 3.0 (2010) ●
    Modified cardinality of &lt;ProductRelationCode&gt; at revision 3.0 (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    product_relation_code: list[ProductRelationCode] = field(
        default_factory=list,
        metadata={
            "name": "ProductRelationCode",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    product_identifier: list[ProductIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ProductIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    product_form: Optional[ProductForm] = field(
        default=None,
        metadata={
            "name": "ProductForm",
            "type": "Element",
        },
    )
    product_form_detail: list[ProductFormDetail] = field(
        default_factory=list,
        metadata={
            "name": "ProductFormDetail",
            "type": "Element",
        },
    )
    refname: Optional[RelatedProductRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[RelatedProductShortname] = field(
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
