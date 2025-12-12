from dataclasses import dataclass, field
from typing import Optional

from .b374 import B374
from .contentdate import Contentdate
from .d104 import D104
from .d107 import D107
from .list3 import List3
from .reviewrating import Reviewrating
from .territory import Territory
from .textcontent_refname import TextcontentRefname
from .textcontent_shortname import TextcontentShortname
from .x426 import X426
from .x427 import X427
from .x428 import X428
from .x557 import X557

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Textcontent:
    """
    Details of a supporting text, primarily for marketing and promotional purposes
    ● Added &lt;TextSourceDescription&gt; at revision 3.0.7 ● Added
    &lt;Territory&gt;, &lt;ReviewRating&gt; at revision 3.0.3 ● Modified
    cardinality of &lt;SourceTitle&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;Text&gt; at revision 3.0.1.
    """

    class Meta:
        name = "textcontent"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x426: Optional[X426] = field(
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
            "min_occurs": 1,
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    d104: list[D104] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    reviewrating: Optional[Reviewrating] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    d107: list[D107] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b374: Optional[B374] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x557: list[X557] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x428: list[X428] = field(
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
    refname: Optional[TextcontentRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TextcontentShortname] = field(
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
