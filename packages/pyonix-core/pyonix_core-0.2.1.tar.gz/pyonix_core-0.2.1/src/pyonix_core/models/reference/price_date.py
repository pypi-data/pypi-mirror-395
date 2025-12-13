from dataclasses import dataclass, field
from typing import Optional

from .date import Date
from .date_format import DateFormat
from .list3 import List3
from .price_date_refname import PriceDateRefname
from .price_date_role import PriceDateRole
from .price_date_shortname import PriceDateShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class PriceDate:
    """
    Date of the specified role relating to the price ● Modified cardinality of
    &lt;DateFormat&gt; at revision 3.0 (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    price_date_role: Optional[PriceDateRole] = field(
        default=None,
        metadata={
            "name": "PriceDateRole",
            "type": "Element",
            "required": True,
        },
    )
    date_format: Optional[DateFormat] = field(
        default=None,
        metadata={
            "name": "DateFormat",
            "type": "Element",
        },
    )
    date: Optional[Date] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[PriceDateRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PriceDateShortname] = field(
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
