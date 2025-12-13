from dataclasses import dataclass, field
from typing import Optional

from .barcode import Barcode
from .collateral_detail import CollateralDetail
from .content_detail import ContentDetail
from .deletion_text import DeletionText
from .descriptive_detail import DescriptiveDetail
from .list3 import List3
from .notification_type import NotificationType
from .product_identifier import ProductIdentifier
from .product_refname import ProductRefname
from .product_shortname import ProductShortname
from .product_supply import ProductSupply
from .production_detail import ProductionDetail
from .promotion_detail import PromotionDetail
from .publishing_detail import PublishingDetail
from .record_reference import RecordReference
from .record_source_identifier import RecordSourceIdentifier
from .record_source_name import RecordSourceName
from .record_source_type import RecordSourceType
from .related_material import RelatedMaterial

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Product:
    """
    Container for details of a single product ● Added &lt;ProductionDetail&gt;
    (Block 8) at revision 3.0.8 ● Added &lt;PromotionDetail&gt; (Block 7) at
    revision 3.0.7 ● Modified cardinality of &lt;DeletionText&gt; at revision
    3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    record_reference: Optional[RecordReference] = field(
        default=None,
        metadata={
            "name": "RecordReference",
            "type": "Element",
            "required": True,
        },
    )
    notification_type: Optional[NotificationType] = field(
        default=None,
        metadata={
            "name": "NotificationType",
            "type": "Element",
            "required": True,
        },
    )
    deletion_text: list[DeletionText] = field(
        default_factory=list,
        metadata={
            "name": "DeletionText",
            "type": "Element",
        },
    )
    record_source_type: Optional[RecordSourceType] = field(
        default=None,
        metadata={
            "name": "RecordSourceType",
            "type": "Element",
        },
    )
    record_source_identifier: list[RecordSourceIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "RecordSourceIdentifier",
            "type": "Element",
        },
    )
    record_source_name: Optional[RecordSourceName] = field(
        default=None,
        metadata={
            "name": "RecordSourceName",
            "type": "Element",
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
    barcode: list[Barcode] = field(
        default_factory=list,
        metadata={
            "name": "Barcode",
            "type": "Element",
        },
    )
    descriptive_detail: Optional[DescriptiveDetail] = field(
        default=None,
        metadata={
            "name": "DescriptiveDetail",
            "type": "Element",
        },
    )
    collateral_detail: Optional[CollateralDetail] = field(
        default=None,
        metadata={
            "name": "CollateralDetail",
            "type": "Element",
        },
    )
    promotion_detail: Optional[PromotionDetail] = field(
        default=None,
        metadata={
            "name": "PromotionDetail",
            "type": "Element",
        },
    )
    content_detail: Optional[ContentDetail] = field(
        default=None,
        metadata={
            "name": "ContentDetail",
            "type": "Element",
        },
    )
    publishing_detail: Optional[PublishingDetail] = field(
        default=None,
        metadata={
            "name": "PublishingDetail",
            "type": "Element",
        },
    )
    related_material: Optional[RelatedMaterial] = field(
        default=None,
        metadata={
            "name": "RelatedMaterial",
            "type": "Element",
        },
    )
    production_detail: Optional[ProductionDetail] = field(
        default=None,
        metadata={
            "name": "ProductionDetail",
            "type": "Element",
        },
    )
    product_supply: list[ProductSupply] = field(
        default_factory=list,
        metadata={
            "name": "ProductSupply",
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
