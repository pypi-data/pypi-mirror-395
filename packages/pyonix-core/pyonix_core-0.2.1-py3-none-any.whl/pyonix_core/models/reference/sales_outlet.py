from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .sales_outlet_identifier import SalesOutletIdentifier
from .sales_outlet_name import SalesOutletName
from .sales_outlet_refname import SalesOutletRefname
from .sales_outlet_shortname import SalesOutletShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SalesOutlet:
    """
    Details of a specific retail outlet, eg one associated with sales exclusivity.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sales_outlet_identifier: list[SalesOutletIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "SalesOutletIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    sales_outlet_name: list[SalesOutletName] = field(
        default_factory=list,
        metadata={
            "name": "SalesOutletName",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    refname: Optional[SalesOutletRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SalesOutletShortname] = field(
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
