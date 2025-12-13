from dataclasses import dataclass, field
from typing import Optional

from .city_of_publication import CityOfPublication
from .copyright_statement import CopyrightStatement
from .country_of_publication import CountryOfPublication
from .imprint import Imprint
from .latest_reprint_number import LatestReprintNumber
from .list3 import List3
from .product_contact import ProductContact
from .publisher import Publisher
from .publishing_date import PublishingDate
from .publishing_detail_refname import PublishingDetailRefname
from .publishing_detail_shortname import PublishingDetailShortname
from .publishing_status import PublishingStatus
from .publishing_status_note import PublishingStatusNote
from .rowsales_rights_type import RowsalesRightsType
from .sales_restriction import SalesRestriction
from .sales_rights import SalesRights

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class PublishingDetail:
    """
    Block 4, container for information about describing branding, publishing and
    rights attached to the product ● Added &lt;ProductContact&gt; at revision 3.0.1
    ● Modified cardinality of &lt;PublishingStatusNote&gt; at revision 3.0.1 ●
    Added &lt;ROWSalesRightsType&gt; at revision 3.0 (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    imprint: list[Imprint] = field(
        default_factory=list,
        metadata={
            "name": "Imprint",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    publisher: list[Publisher] = field(
        default_factory=list,
        metadata={
            "name": "Publisher",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    city_of_publication: list[CityOfPublication] = field(
        default_factory=list,
        metadata={
            "name": "CityOfPublication",
            "type": "Element",
        },
    )
    country_of_publication: Optional[CountryOfPublication] = field(
        default=None,
        metadata={
            "name": "CountryOfPublication",
            "type": "Element",
        },
    )
    product_contact: list[ProductContact] = field(
        default_factory=list,
        metadata={
            "name": "ProductContact",
            "type": "Element",
        },
    )
    publishing_status: Optional[PublishingStatus] = field(
        default=None,
        metadata={
            "name": "PublishingStatus",
            "type": "Element",
        },
    )
    publishing_status_note: list[PublishingStatusNote] = field(
        default_factory=list,
        metadata={
            "name": "PublishingStatusNote",
            "type": "Element",
        },
    )
    publishing_date: list[PublishingDate] = field(
        default_factory=list,
        metadata={
            "name": "PublishingDate",
            "type": "Element",
        },
    )
    latest_reprint_number: Optional[LatestReprintNumber] = field(
        default=None,
        metadata={
            "name": "LatestReprintNumber",
            "type": "Element",
        },
    )
    copyright_statement: list[CopyrightStatement] = field(
        default_factory=list,
        metadata={
            "name": "CopyrightStatement",
            "type": "Element",
        },
    )
    sales_rights: list[SalesRights] = field(
        default_factory=list,
        metadata={
            "name": "SalesRights",
            "type": "Element",
        },
    )
    rowsales_rights_type: Optional[RowsalesRightsType] = field(
        default=None,
        metadata={
            "name": "ROWSalesRightsType",
            "type": "Element",
        },
    )
    sales_restriction: list[SalesRestriction] = field(
        default_factory=list,
        metadata={
            "name": "SalesRestriction",
            "type": "Element",
        },
    )
    refname: Optional[PublishingDetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PublishingDetailShortname] = field(
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
