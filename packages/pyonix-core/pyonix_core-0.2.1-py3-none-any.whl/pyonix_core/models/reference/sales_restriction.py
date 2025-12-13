from dataclasses import dataclass, field
from typing import Optional

from .end_date import EndDate
from .list3 import List3
from .sales_outlet import SalesOutlet
from .sales_restriction_note import SalesRestrictionNote
from .sales_restriction_refname import SalesRestrictionRefname
from .sales_restriction_shortname import SalesRestrictionShortname
from .sales_restriction_type import SalesRestrictionType
from .start_date import StartDate

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SalesRestriction:
    """
    Details of a non-geographical restriction on sales, applicable with the
    associated sales rights territory or market ● Deprecated P.21.11–21.18 at
    revision 3.0.2, in favour of using &lt;SalesRestriction within
    &lt;SalesRights&gt; (P.21.5a) ● Modified cardinality of
    &lt;SalesRestrictionNote&gt; at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sales_restriction_type: Optional[SalesRestrictionType] = field(
        default=None,
        metadata={
            "name": "SalesRestrictionType",
            "type": "Element",
            "required": True,
        },
    )
    sales_outlet: list[SalesOutlet] = field(
        default_factory=list,
        metadata={
            "name": "SalesOutlet",
            "type": "Element",
        },
    )
    sales_restriction_note: list[SalesRestrictionNote] = field(
        default_factory=list,
        metadata={
            "name": "SalesRestrictionNote",
            "type": "Element",
        },
    )
    start_date: Optional[StartDate] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
        },
    )
    end_date: Optional[EndDate] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Element",
        },
    )
    refname: Optional[SalesRestrictionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SalesRestrictionShortname] = field(
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
