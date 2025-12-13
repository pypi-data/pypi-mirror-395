from dataclasses import dataclass, field
from typing import Optional

from .epubusageconstraint_refname import EpubusageconstraintRefname
from .epubusageconstraint_shortname import EpubusageconstraintShortname
from .epubusagelimit import Epubusagelimit
from .list3 import List3
from .x318 import X318
from .x319 import X319

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Epubusageconstraint:
    """
    Details of a limitation on usage of a digital product (whether or not this
    constraint is enforced by DRM)
    """

    class Meta:
        name = "epubusageconstraint"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x318: Optional[X318] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x319: Optional[X319] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    epubusagelimit: list[Epubusagelimit] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[EpubusageconstraintRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[EpubusageconstraintShortname] = field(
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
