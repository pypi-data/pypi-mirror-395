from dataclasses import dataclass, field
from typing import Optional

from .addressee import Addressee
from .header_refname import HeaderRefname
from .header_shortname import HeaderShortname
from .list3 import List3
from .m180 import M180
from .m181 import M181
from .m183 import M183
from .m184 import M184
from .m186 import M186
from .sender import Sender
from .x307 import X307
from .x310 import X310

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Header:
    """
    Container for message metadata ● Modified cardinality of &lt;MessageNote&gt; at
    revision 3.0.1.
    """

    class Meta:
        name = "header"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    sender: Optional[Sender] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    addressee: list[Addressee] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    m180: Optional[M180] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    m181: Optional[M181] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x307: Optional[X307] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    m183: list[M183] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    m184: Optional[M184] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x310: Optional[X310] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    m186: Optional[M186] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[HeaderRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[HeaderShortname] = field(
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
