from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .related_material_refname import RelatedMaterialRefname
from .related_material_shortname import RelatedMaterialShortname
from .related_product import RelatedProduct
from .related_work import RelatedWork

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class RelatedMaterial:
    """
    Block 5, container for elements providing links to closely-related products and
    works.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    related_work: list[RelatedWork] = field(
        default_factory=list,
        metadata={
            "name": "RelatedWork",
            "type": "Element",
        },
    )
    related_product: list[RelatedProduct] = field(
        default_factory=list,
        metadata={
            "name": "RelatedProduct",
            "type": "Element",
        },
    )
    refname: Optional[RelatedMaterialRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[RelatedMaterialShortname] = field(
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
