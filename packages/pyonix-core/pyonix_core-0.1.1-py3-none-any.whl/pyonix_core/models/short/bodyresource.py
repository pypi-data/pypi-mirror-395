from dataclasses import dataclass, field
from typing import Optional

from .b034 import B034
from .bodyresource_refname import BodyresourceRefname
from .bodyresource_shortname import BodyresourceShortname
from .list3 import List3
from .resourcefiledate import Resourcefiledate
from .resourcefilefeature import Resourcefilefeature
from .resourceidentifier import Resourceidentifier
from .x566 import X566
from .x567 import X567
from .x571 import X571
from .x572 import X572
from .x576 import X576

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Bodyresource:
    """
    Details of a resource file needed to manufacture or package the main body of a
    product ● Added at revision 3.0.8.
    """

    class Meta:
        name = "bodyresource"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b034: Optional[B034] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    resourceidentifier: list[Resourceidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x566: Optional[X566] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x567: list[X567] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    resourcefilefeature: list[Resourcefilefeature] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x571: list[X571] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x576: list[X576] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x572: list[X572] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    resourcefiledate: list[Resourcefiledate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[BodyresourceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[BodyresourceShortname] = field(
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
