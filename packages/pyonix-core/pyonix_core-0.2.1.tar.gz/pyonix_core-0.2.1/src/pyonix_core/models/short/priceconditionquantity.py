from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .priceconditionquantity_refname import PriceconditionquantityRefname
from .priceconditionquantity_shortname import PriceconditionquantityShortname
from .x320 import X320
from .x464 import X464
from .x466 import X466

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Priceconditionquantity:
    class Meta:
        name = "priceconditionquantity"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x464: Optional[X464] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x320: Optional[X320] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x466: Optional[X466] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[PriceconditionquantityRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PriceconditionquantityShortname] = field(
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
