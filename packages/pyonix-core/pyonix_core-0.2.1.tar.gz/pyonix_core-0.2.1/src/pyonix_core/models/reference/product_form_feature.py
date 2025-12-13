from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .product_form_feature_description import ProductFormFeatureDescription
from .product_form_feature_refname import ProductFormFeatureRefname
from .product_form_feature_shortname import ProductFormFeatureShortname
from .product_form_feature_type import ProductFormFeatureType
from .product_form_feature_value import ProductFormFeatureValue

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ProductFormFeature:
    """Additional detail of the digital or physical nature of the product and its
    features, in addition to the &lt;ProductForm&gt; and &lt;ProductFormDetail&gt;.

    Repeatable if multiple different details are provided ● Modified
    cardinality of &lt;ProductFormFeatureDescription&gt; at revision
    3.0.1
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    product_form_feature_type: Optional[ProductFormFeatureType] = field(
        default=None,
        metadata={
            "name": "ProductFormFeatureType",
            "type": "Element",
            "required": True,
        },
    )
    product_form_feature_value: Optional[ProductFormFeatureValue] = field(
        default=None,
        metadata={
            "name": "ProductFormFeatureValue",
            "type": "Element",
        },
    )
    product_form_feature_description: list[ProductFormFeatureDescription] = (
        field(
            default_factory=list,
            metadata={
                "name": "ProductFormFeatureDescription",
                "type": "Element",
            },
        )
    )
    refname: Optional[ProductFormFeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductFormFeatureShortname] = field(
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
