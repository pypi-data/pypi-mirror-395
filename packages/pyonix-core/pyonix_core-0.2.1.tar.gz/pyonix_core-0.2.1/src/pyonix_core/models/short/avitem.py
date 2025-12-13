from dataclasses import dataclass, field
from typing import Optional

from .avitem_refname import AvitemRefname
from .avitem_shortname import AvitemShortname
from .avitemidentifier import Avitemidentifier
from .list3 import List3
from .timerun import Timerun
from .x540 import X540
from .x544 import X544

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Avitem:
    """
    Details of an audiovisual content item (eg a chapter) ● Added at revision
    3.0.5.
    """

    class Meta:
        name = "avitem"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x540: Optional[X540] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    avitemidentifier: list[Avitemidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    timerun: list[Timerun] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x544: Optional[X544] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[AvitemRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[AvitemShortname] = field(
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
