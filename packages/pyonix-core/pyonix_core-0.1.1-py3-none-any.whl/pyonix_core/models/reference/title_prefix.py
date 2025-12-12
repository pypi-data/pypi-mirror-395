from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .list14 import List14
from .list74 import List74
from .list121 import List121
from .title_prefix_refname import TitlePrefixRefname
from .title_prefix_shortname import TitlePrefixShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class TitlePrefix:
    """
    Prefix at the beginning of a title element which is ignored for sorting
    purposes, eg An, The ● Added language attribute at revision 3.0.2 ● Added
    collationkey, textscript attributes at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\S(.*\S)?",
        },
    )
    refname: Optional[TitlePrefixRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TitlePrefixShortname] = field(
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
    collationkey: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"\S(.*\S)?",
        },
    )
    language: Optional[List74] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    textscript: Optional[List121] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    textcase: Optional[List14] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
