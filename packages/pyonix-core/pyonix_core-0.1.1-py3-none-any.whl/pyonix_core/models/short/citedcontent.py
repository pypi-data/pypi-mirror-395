from dataclasses import dataclass, field
from typing import Optional

from .citedcontent_refname import CitedcontentRefname
from .citedcontent_shortname import CitedcontentShortname
from .contentdate import Contentdate
from .list3 import List3
from .reviewrating import Reviewrating
from .territory import Territory
from .x427 import X427
from .x428 import X428
from .x430 import X430
from .x431 import X431
from .x432 import X432
from .x433 import X433
from .x434 import X434
from .x435 import X435

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Citedcontent:
    """
    Third-party material which may be cited primarily for marketing and promotional
    purposes ● Added &lt;Territory&gt;, &lt;ReviewRating&gt; at revision 3.0.3 ●
    Modified cardinality of &lt;ListName&gt;, &lt;SourceTitle&gt; at revision 3.0.2
    ● Modified cardinality of &lt;CitationNote&gt; at revision 3.0.1.
    """

    class Meta:
        name = "citedcontent"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x430: Optional[X430] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x427: list[X427] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x431: Optional[X431] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    reviewrating: Optional[Reviewrating] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x428: list[X428] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 2,
            "sequence": 1,
        },
    )
    x432: list[X432] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x433: list[X433] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 2,
        },
    )
    x434: list[X434] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x435: list[X435] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    contentdate: list[Contentdate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[CitedcontentRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CitedcontentShortname] = field(
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
