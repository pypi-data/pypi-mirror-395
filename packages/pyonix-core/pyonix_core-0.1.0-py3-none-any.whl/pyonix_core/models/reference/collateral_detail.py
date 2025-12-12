from dataclasses import dataclass, field
from typing import Optional

from .cited_content import CitedContent
from .collateral_detail_refname import CollateralDetailRefname
from .collateral_detail_shortname import CollateralDetailShortname
from .list3 import List3
from .prize import Prize
from .supporting_resource import SupportingResource
from .text_content import TextContent

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class CollateralDetail:
    """
    Block 2, container for information and resources to support marketing the
    product.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    text_content: list[TextContent] = field(
        default_factory=list,
        metadata={
            "name": "TextContent",
            "type": "Element",
        },
    )
    cited_content: list[CitedContent] = field(
        default_factory=list,
        metadata={
            "name": "CitedContent",
            "type": "Element",
        },
    )
    supporting_resource: list[SupportingResource] = field(
        default_factory=list,
        metadata={
            "name": "SupportingResource",
            "type": "Element",
        },
    )
    prize: list[Prize] = field(
        default_factory=list,
        metadata={
            "name": "Prize",
            "type": "Element",
        },
    )
    refname: Optional[CollateralDetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CollateralDetailShortname] = field(
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
