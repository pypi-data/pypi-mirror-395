from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .timerun_refname import TimerunRefname
from .timerun_shortname import TimerunShortname
from .x542 import X542
from .x543 import X543

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Timerun:
    """
    Details of the start and end times of an audiovisual content item ● Added at
    revision 3.0.5.
    """

    class Meta:
        name = "timerun"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x542: Optional[X542] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x543: Optional[X543] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[TimerunRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TimerunShortname] = field(
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
