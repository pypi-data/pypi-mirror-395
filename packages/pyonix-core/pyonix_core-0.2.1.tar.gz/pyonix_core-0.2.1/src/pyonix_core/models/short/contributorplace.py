from dataclasses import dataclass, field
from typing import Optional

from .b251 import B251
from .b398 import B398
from .contributorplace_refname import ContributorplaceRefname
from .contributorplace_shortname import ContributorplaceShortname
from .j349 import J349
from .list3 import List3
from .x418 import X418

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Contributorplace:
    """
    Location with which a contributor is associated ● Added &lt;LocationName&gt; at
    revision 3.0.2.
    """

    class Meta:
        name = "contributorplace"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x418: Optional[X418] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b251: Optional[B251] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b398: list[B398] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    j349: list[J349] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ContributorplaceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ContributorplaceShortname] = field(
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
