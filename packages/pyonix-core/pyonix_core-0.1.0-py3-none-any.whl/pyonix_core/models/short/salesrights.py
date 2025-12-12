from dataclasses import dataclass, field
from typing import Optional

from .b081 import B081
from .b089 import B089
from .list3 import List3
from .productidentifier import Productidentifier
from .salesrestriction import Salesrestriction
from .salesrights_refname import SalesrightsRefname
from .salesrights_shortname import SalesrightsShortname
from .territory import Territory

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Salesrights:
    """
    Details of a geographical territory and the sales rights and restriction that
    apply in that territory ● Added &lt;SalesRestriction&gt; at revision 3.0.2.
    """

    class Meta:
        name = "salesrights"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b089: Optional[B089] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    salesrestriction: list[Salesrestriction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    productidentifier: list[Productidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b081: Optional[B081] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[SalesrightsRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SalesrightsShortname] = field(
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
