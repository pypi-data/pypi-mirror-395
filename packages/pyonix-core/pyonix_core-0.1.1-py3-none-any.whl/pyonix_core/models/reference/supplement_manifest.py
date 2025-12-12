from dataclasses import dataclass, field
from typing import Optional

from .body_manifest import BodyManifest
from .cover_manifest import CoverManifest
from .insert_manifest import InsertManifest
from .list3 import List3
from .measure import Measure
from .no_supplement import NoSupplement
from .product_form import ProductForm
from .product_form_description import ProductFormDescription
from .product_form_detail import ProductFormDetail
from .product_identifier import ProductIdentifier
from .sales_outlet import SalesOutlet
from .sequence_number import SequenceNumber
from .supplement_manifest_refname import SupplementManifestRefname
from .supplement_manifest_shortname import SupplementManifestShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SupplementManifest:
    """
    Details of the resource files needed to manufacture or package a supplement to
    a product ● Added at revision 3.0.8.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sequence_number: Optional[SequenceNumber] = field(
        default=None,
        metadata={
            "name": "SequenceNumber",
            "type": "Element",
        },
    )
    sales_outlet: list[SalesOutlet] = field(
        default_factory=list,
        metadata={
            "name": "SalesOutlet",
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
        },
    )
    product_form_detail: list[ProductFormDetail] = field(
        default_factory=list,
        metadata={
            "name": "ProductFormDetail",
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
    measure: list[Measure] = field(
        default_factory=list,
        metadata={
            "name": "Measure",
            "type": "Element",
        },
    )
    cover_manifest: Optional[CoverManifest] = field(
        default=None,
        metadata={
            "name": "CoverManifest",
            "type": "Element",
        },
    )
    body_manifest: Optional[BodyManifest] = field(
        default=None,
        metadata={
            "name": "BodyManifest",
            "type": "Element",
        },
    )
    insert_manifest: list[InsertManifest] = field(
        default_factory=list,
        metadata={
            "name": "InsertManifest",
            "type": "Element",
        },
    )
    no_supplement: Optional[NoSupplement] = field(
        default=None,
        metadata={
            "name": "NoSupplement",
            "type": "Element",
        },
    )
    refname: Optional[SupplementManifestRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SupplementManifestShortname] = field(
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
