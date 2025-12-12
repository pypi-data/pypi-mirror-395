from dataclasses import dataclass, field
from typing import Optional

from .b247_refname import B247Refname
from .b247_shortname import B247Shortname
from .list3 import List3
from .list74 import List74
from .list121 import List121

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class B247:
    """
    Part of a structured name (of a person or persona) – prefix to the key names
    (eg ‘de la’ or ‘van’) ignored for alphabetic sorting purposes ● Added language
    attribute at revision 3.0.2 ● Added collationkey, textscript attributes at
    revision 3.0.1.
    """

    class Meta:
        name = "b247"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\S(.*\S)?",
        },
    )
    refname: Optional[B247Refname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[B247Shortname] = field(
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
    textscript: Optional[List121] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    language: Optional[List74] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
