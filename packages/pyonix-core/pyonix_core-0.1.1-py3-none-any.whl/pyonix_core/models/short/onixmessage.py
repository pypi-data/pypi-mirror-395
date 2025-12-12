from dataclasses import dataclass, field
from typing import Optional

from .header import Header
from .list3 import List3
from .onixmessage_refname import OnixmessageRefname
from .onixmessage_release import OnixmessageRelease
from .onixmessage_shortname import OnixmessageShortname
from .product import Product
from .x507 import X507

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Onixmessage:
    """
    Root element – the top level container within an ONIX message ● Added
    &lt;NoProduct&gt; at revision 3.0.2.
    """

    class Meta:
        name = "ONIXmessage"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    header: Optional[Header] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x507: Optional[X507] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    product: list[Product] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[OnixmessageRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[OnixmessageShortname] = field(
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
    release: Optional[OnixmessageRelease] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
