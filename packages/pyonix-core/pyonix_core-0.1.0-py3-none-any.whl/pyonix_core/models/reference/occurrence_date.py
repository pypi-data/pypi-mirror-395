from dataclasses import dataclass, field
from typing import Optional

from .date import Date
from .date_format import DateFormat
from .list3 import List3
from .occurrence_date_refname import OccurrenceDateRefname
from .occurrence_date_role import OccurrenceDateRole
from .occurrence_date_shortname import OccurrenceDateShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class OccurrenceDate:
    """
    Date related to an occurrence of a promotional event ● Added at revision 3.0.7.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    occurrence_date_role: Optional[OccurrenceDateRole] = field(
        default=None,
        metadata={
            "name": "OccurrenceDateRole",
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
    refname: Optional[OccurrenceDateRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[OccurrenceDateShortname] = field(
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
