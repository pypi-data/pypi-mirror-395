from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .product_identifier import ProductIdentifier
from .publisher_name import PublisherName
from .sales_restriction import SalesRestriction
from .sales_rights_refname import SalesRightsRefname
from .sales_rights_shortname import SalesRightsShortname
from .sales_rights_type import SalesRightsType
from .territory import Territory

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SalesRights:
    """
    Details of a geographical territory and the sales rights and restriction that
    apply in that territory ● Added &lt;SalesRestriction&gt; at revision 3.0.2.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sales_rights_type: Optional[SalesRightsType] = field(
        default=None,
        metadata={
            "name": "SalesRightsType",
            "type": "Element",
            "required": True,
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "name": "Territory",
            "type": "Element",
            "required": True,
        },
    )
    sales_restriction: list[SalesRestriction] = field(
        default_factory=list,
        metadata={
            "name": "SalesRestriction",
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
    publisher_name: Optional[PublisherName] = field(
        default=None,
        metadata={
            "name": "PublisherName",
            "type": "Element",
        },
    )
    refname: Optional[SalesRightsRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SalesRightsShortname] = field(
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
