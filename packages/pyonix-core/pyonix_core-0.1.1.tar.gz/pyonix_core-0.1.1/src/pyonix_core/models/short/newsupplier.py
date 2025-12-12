from dataclasses import dataclass, field
from typing import Optional

from .j137 import J137
from .j270 import J270
from .j271 import J271
from .j272 import J272
from .list3 import List3
from .newsupplier_refname import NewsupplierRefname
from .newsupplier_shortname import NewsupplierShortname
from .supplieridentifier import Supplieridentifier

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Newsupplier:
    class Meta:
        name = "newsupplier"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    supplieridentifier: list[Supplieridentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    j137: list[J137] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    j270: list[J270] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j271: list[J271] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j272: list[J272] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[NewsupplierRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[NewsupplierShortname] = field(
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
