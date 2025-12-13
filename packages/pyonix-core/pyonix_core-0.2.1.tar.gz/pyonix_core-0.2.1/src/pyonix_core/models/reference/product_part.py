from dataclasses import dataclass, field
from typing import Optional

from .country_of_manufacture import CountryOfManufacture
from .list3 import List3
from .measure import Measure
from .number_of_copies import NumberOfCopies
from .number_of_items_of_this_form import NumberOfItemsOfThisForm
from .primary_part import PrimaryPart
from .product_content_type import ProductContentType
from .product_form import ProductForm
from .product_form_description import ProductFormDescription
from .product_form_detail import ProductFormDetail
from .product_form_feature import ProductFormFeature
from .product_identifier import ProductIdentifier
from .product_packaging import ProductPackaging
from .product_part_refname import ProductPartRefname
from .product_part_shortname import ProductPartShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ProductPart:
    """Details of a component which comprises part of the product.

    Note that components may also be product items in their own right ●
    Added &lt;Measure&gt; at revision 3.0.6 ● Added
    &lt;ProductPckaging&gt; at revision 3.0.3 ● Modified cardinality of
    &lt;ProductFormDescription&gt; at revision 3.0.1
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    primary_part: Optional[PrimaryPart] = field(
        default=None,
        metadata={
            "name": "PrimaryPart",
            "type": "Element",
        },
    )
    product_identifier: list[ProductIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ProductIdentifier",
            "type": "Element",
        },
    )
    product_form: Optional[ProductForm] = field(
        default=None,
        metadata={
            "name": "ProductForm",
            "type": "Element",
            "required": True,
        },
    )
    product_form_detail: list[ProductFormDetail] = field(
        default_factory=list,
        metadata={
            "name": "ProductFormDetail",
            "type": "Element",
        },
    )
    product_form_feature: list[ProductFormFeature] = field(
        default_factory=list,
        metadata={
            "name": "ProductFormFeature",
            "type": "Element",
        },
    )
    product_packaging: Optional[ProductPackaging] = field(
        default=None,
        metadata={
            "name": "ProductPackaging",
            "type": "Element",
        },
    )
    product_form_description: list[ProductFormDescription] = field(
        default_factory=list,
        metadata={
            "name": "ProductFormDescription",
            "type": "Element",
        },
    )
    product_content_type: list[ProductContentType] = field(
        default_factory=list,
        metadata={
            "name": "ProductContentType",
            "type": "Element",
        },
    )
    measure: list[Measure] = field(
        default_factory=list,
        metadata={
            "name": "Measure",
            "type": "Element",
        },
    )
    number_of_items_of_this_form: Optional[NumberOfItemsOfThisForm] = field(
        default=None,
        metadata={
            "name": "NumberOfItemsOfThisForm",
            "type": "Element",
            "required": True,
        },
    )
    number_of_copies: list[NumberOfCopies] = field(
        default_factory=list,
        metadata={
            "name": "NumberOfCopies",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    country_of_manufacture: Optional[CountryOfManufacture] = field(
        default=None,
        metadata={
            "name": "CountryOfManufacture",
            "type": "Element",
        },
    )
    refname: Optional[ProductPartRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductPartShortname] = field(
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
