from dataclasses import dataclass, field
from typing import Optional

from .b352 import B352
from .b353 import B353
from .b354 import B354
from .b355 import B355
from .b356 import B356
from .b357 import B357
from .b389 import B389
from .bible_refname import BibleRefname
from .bible_shortname import BibleShortname
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Bible:
    class Meta:
        name = "bible"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b352: list[B352] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    b353: list[B353] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    b389: Optional[B389] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b354: list[B354] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b355: Optional[B355] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b356: Optional[B356] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b357: list[B357] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[BibleRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[BibleShortname] = field(
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
