from dataclasses import dataclass, field
from typing import Optional

from .extent_refname import ExtentRefname
from .extent_shortname import ExtentShortname
from .extent_type import ExtentType
from .extent_unit import ExtentUnit
from .extent_value import ExtentValue
from .extent_value_roman import ExtentValueRoman
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Extent:
    """
    Details of an extent (eg number of pages, duration) of a product.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    extent_type: Optional[ExtentType] = field(
        default=None,
        metadata={
            "name": "ExtentType",
            "type": "Element",
            "required": True,
        },
    )
    extent_value: Optional[ExtentValue] = field(
        default=None,
        metadata={
            "name": "ExtentValue",
            "type": "Element",
            "required": True,
        },
    )
    extent_value_roman: list[ExtentValueRoman] = field(
        default_factory=list,
        metadata={
            "name": "ExtentValueRoman",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    extent_unit: Optional[ExtentUnit] = field(
        default=None,
        metadata={
            "name": "ExtentUnit",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[ExtentRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ExtentShortname] = field(
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
