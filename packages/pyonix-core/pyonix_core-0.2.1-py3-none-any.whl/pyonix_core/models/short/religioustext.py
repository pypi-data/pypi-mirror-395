from dataclasses import dataclass, field
from typing import Optional

from .b376 import B376
from .bible import Bible
from .list3 import List3
from .religioustext_refname import ReligioustextRefname
from .religioustext_shortname import ReligioustextShortname
from .religioustextfeature import Religioustextfeature

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Religioustext:
    """
    Details of the special features of a religious text, eg the Bible, the Qur’an.
    """

    class Meta:
        name = "religioustext"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    bible: Optional[Bible] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b376: Optional[B376] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    religioustextfeature: list[Religioustextfeature] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ReligioustextRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ReligioustextShortname] = field(
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
