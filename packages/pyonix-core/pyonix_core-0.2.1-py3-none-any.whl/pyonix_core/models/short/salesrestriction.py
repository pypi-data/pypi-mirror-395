from dataclasses import dataclass, field
from typing import Optional

from .b324 import B324
from .b325 import B325
from .b381 import B381
from .list3 import List3
from .salesoutlet import Salesoutlet
from .salesrestriction_refname import SalesrestrictionRefname
from .salesrestriction_shortname import SalesrestrictionShortname
from .x453 import X453

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Salesrestriction:
    """
    Details of a non-geographical restriction on sales, applicable with the
    associated sales rights territory or market ● Deprecated P.21.11–21.18 at
    revision 3.0.2, in favour of using &lt;SalesRestriction within
    &lt;SalesRights&gt; (P.21.5a) ● Modified cardinality of
    &lt;SalesRestrictionNote&gt; at revision 3.0.1.
    """

    class Meta:
        name = "salesrestriction"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b381: Optional[B381] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    salesoutlet: list[Salesoutlet] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x453: list[X453] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b324: Optional[B324] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b325: Optional[B325] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[SalesrestrictionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SalesrestrictionShortname] = field(
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
