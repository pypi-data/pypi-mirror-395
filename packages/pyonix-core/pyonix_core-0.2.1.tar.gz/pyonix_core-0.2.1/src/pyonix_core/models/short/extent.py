from dataclasses import dataclass, field
from typing import Optional

from .b218 import B218
from .b219 import B219
from .b220 import B220
from .extent_refname import ExtentRefname
from .extent_shortname import ExtentShortname
from .list3 import List3
from .x421 import X421

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Extent:
    """
    Details of an extent (eg number of pages, duration) of a product.
    """

    class Meta:
        name = "extent"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b218: Optional[B218] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b219: Optional[B219] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x421: list[X421] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    b220: Optional[B220] = field(
        default=None,
        metadata={
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
