from dataclasses import dataclass, field
from typing import Optional

from .audience_refname import AudienceRefname
from .audience_shortname import AudienceShortname
from .b204 import B204
from .b205 import B205
from .b206 import B206
from .list3 import List3
from .x578 import X578

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Audience:
    """
    Details of a target audience ● Added &lt;AudienceHeadingText&gt; at 3.0.8.
    """

    class Meta:
        name = "audience"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b204: Optional[B204] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b205: Optional[B205] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b206: Optional[B206] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x578: list[X578] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    refname: Optional[AudienceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[AudienceShortname] = field(
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
