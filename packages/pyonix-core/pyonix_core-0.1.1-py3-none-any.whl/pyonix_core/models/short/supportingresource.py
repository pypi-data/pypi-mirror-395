from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .resourcefeature import Resourcefeature
from .resourceversion import Resourceversion
from .supportingresource_refname import SupportingresourceRefname
from .supportingresource_shortname import SupportingresourceShortname
from .territory import Territory
from .x427 import X427
from .x436 import X436
from .x437 import X437

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Supportingresource:
    """
    Details of a supporting resource used for marketing and promotional purposes,
    eg a cover image, author photo, sample of the content ● Added &lt;Territory&gt;
    at revision 3.0.3.
    """

    class Meta:
        name = "supportingresource"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x436: Optional[X436] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x427: list[X427] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x437: Optional[X437] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    resourcefeature: list[Resourcefeature] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    resourceversion: list[Resourceversion] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[SupportingresourceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SupportingresourceShortname] = field(
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
