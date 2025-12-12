from dataclasses import dataclass, field
from typing import Optional

from .citedcontent import Citedcontent
from .collateraldetail_refname import CollateraldetailRefname
from .collateraldetail_shortname import CollateraldetailShortname
from .list3 import List3
from .prize import Prize
from .supportingresource import Supportingresource
from .textcontent import Textcontent

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Collateraldetail:
    """
    Block 2, container for information and resources to support marketing the
    product.
    """

    class Meta:
        name = "collateraldetail"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    textcontent: list[Textcontent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    citedcontent: list[Citedcontent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supportingresource: list[Supportingresource] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    prize: list[Prize] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[CollateraldetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CollateraldetailShortname] = field(
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
