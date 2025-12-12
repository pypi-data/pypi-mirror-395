from dataclasses import dataclass, field
from typing import Optional

from .j407 import J407
from .k165 import K165
from .k166 import K166
from .k167 import K167
from .k168 import K168
from .k169 import K169
from .k309 import K309
from .list3 import List3
from .marketdate import Marketdate
from .marketpublishingdetail_refname import MarketpublishingdetailRefname
from .marketpublishingdetail_shortname import MarketpublishingdetailShortname
from .productcontact import Productcontact
from .publisherrepresentative import Publisherrepresentative
from .x406 import X406

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Marketpublishingdetail:
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
        name = "marketpublishingdetail"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    publisherrepresentative: list[Publisherrepresentative] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    productcontact: list[Productcontact] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j407: Optional[J407] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x406: list[X406] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    marketdate: list[Marketdate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    k165: list[K165] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    k166: Optional[K166] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    k167: list[K167] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    k309: list[K309] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    k168: list[K168] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    k169: list[K169] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[MarketpublishingdetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[MarketpublishingdetailShortname] = field(
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
