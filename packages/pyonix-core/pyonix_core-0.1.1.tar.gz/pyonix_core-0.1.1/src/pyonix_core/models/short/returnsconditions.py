from dataclasses import dataclass, field
from typing import Optional

from .j268 import J268
from .j269 import J269
from .list3 import List3
from .returnsconditions_refname import ReturnsconditionsRefname
from .returnsconditions_shortname import ReturnsconditionsShortname
from .x460 import X460
from .x528 import X528

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Returnsconditions:
    """
    Details of the supplier’s returns conditions ● Added &lt;ReturnsNote&gt; at
    revision 3.0.3.
    """

    class Meta:
        name = "returnsconditions"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    j268: Optional[J268] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x460: Optional[X460] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j269: Optional[J269] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x528: list[X528] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ReturnsconditionsRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ReturnsconditionsShortname] = field(
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
