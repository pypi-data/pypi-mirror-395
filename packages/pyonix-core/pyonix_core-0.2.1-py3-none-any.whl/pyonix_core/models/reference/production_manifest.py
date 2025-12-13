from dataclasses import dataclass, field
from typing import Optional

from .body_manifest import BodyManifest
from .cover_manifest import CoverManifest
from .insert_manifest import InsertManifest
from .list3 import List3
from .product_identifier import ProductIdentifier
from .production_manifest_refname import ProductionManifestRefname
from .production_manifest_shortname import ProductionManifestShortname
from .supplement_manifest import SupplementManifest

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ProductionManifest:
    """
    Container for a file manifest and manufacturing specification for a product or
    product part ● Added at revision 3.0.8.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    product_identifier: list[ProductIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ProductIdentifier",
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
            "required": True,
        },
    )
    insert_manifest: list[InsertManifest] = field(
        default_factory=list,
        metadata={
            "name": "InsertManifest",
            "type": "Element",
        },
    )
    supplement_manifest: list[SupplementManifest] = field(
        default_factory=list,
        metadata={
            "name": "SupplementManifest",
            "type": "Element",
        },
    )
    refname: Optional[ProductionManifestRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductionManifestShortname] = field(
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
