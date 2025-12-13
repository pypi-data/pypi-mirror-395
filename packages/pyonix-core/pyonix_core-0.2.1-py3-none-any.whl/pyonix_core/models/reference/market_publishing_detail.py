from dataclasses import dataclass, field
from typing import Optional

from .book_club_adoption import BookClubAdoption
from .copies_sold import CopiesSold
from .initial_print_run import InitialPrintRun
from .list3 import List3
from .market_date import MarketDate
from .market_publishing_detail_refname import MarketPublishingDetailRefname
from .market_publishing_detail_shortname import MarketPublishingDetailShortname
from .market_publishing_status import MarketPublishingStatus
from .market_publishing_status_note import MarketPublishingStatusNote
from .product_contact import ProductContact
from .promotion_campaign import PromotionCampaign
from .promotion_contact import PromotionContact
from .publisher_representative import PublisherRepresentative
from .reprint_detail import ReprintDetail

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class MarketPublishingDetail:
    """
    Details of the market-specific publishing status, associated dates and
    publisher representation for the product within a ‘market’, particular where
    they differ from the relevant details in Block 4 ● Modified cardinality of
    &lt;PromotionCampaign&gt;, &lt;InitialPrintRun&gt;, &lt;CopiesSold&gt;,
    &lt;BookClubAdoption&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;MarketPublishingStatusNote&gt; at revision 3.0.1 ● Modified cardinality of
    &lt;MarketDate&gt; at revision 3.0 (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    publisher_representative: list[PublisherRepresentative] = field(
        default_factory=list,
        metadata={
            "name": "PublisherRepresentative",
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
    market_publishing_status: Optional[MarketPublishingStatus] = field(
        default=None,
        metadata={
            "name": "MarketPublishingStatus",
            "type": "Element",
            "required": True,
        },
    )
    market_publishing_status_note: list[MarketPublishingStatusNote] = field(
        default_factory=list,
        metadata={
            "name": "MarketPublishingStatusNote",
            "type": "Element",
        },
    )
    market_date: list[MarketDate] = field(
        default_factory=list,
        metadata={
            "name": "MarketDate",
            "type": "Element",
        },
    )
    promotion_campaign: list[PromotionCampaign] = field(
        default_factory=list,
        metadata={
            "name": "PromotionCampaign",
            "type": "Element",
        },
    )
    promotion_contact: Optional[PromotionContact] = field(
        default=None,
        metadata={
            "name": "PromotionContact",
            "type": "Element",
        },
    )
    initial_print_run: list[InitialPrintRun] = field(
        default_factory=list,
        metadata={
            "name": "InitialPrintRun",
            "type": "Element",
        },
    )
    reprint_detail: list[ReprintDetail] = field(
        default_factory=list,
        metadata={
            "name": "ReprintDetail",
            "type": "Element",
        },
    )
    copies_sold: list[CopiesSold] = field(
        default_factory=list,
        metadata={
            "name": "CopiesSold",
            "type": "Element",
        },
    )
    book_club_adoption: list[BookClubAdoption] = field(
        default_factory=list,
        metadata={
            "name": "BookClubAdoption",
            "type": "Element",
        },
    )
    refname: Optional[MarketPublishingDetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[MarketPublishingDetailShortname] = field(
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
