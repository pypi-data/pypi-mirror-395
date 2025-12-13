from dataclasses import dataclass, field
from typing import Optional

from .b233 import B233
from .b244 import B244
from .list3 import List3
from .resourceidentifier_refname import ResourceidentifierRefname
from .resourceidentifier_shortname import ResourceidentifierShortname
from .x565 import X565

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Resourceidentifier:
    """Unique identifier for a resource required for manufacturing or packaging of
    the product.

    Note this is likely to be a proprietary identifer used for
    disambiguation by the resource creator ● Added at revision 3.0.8
    """

    class Meta:
        name = "resourceidentifier"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x565: Optional[X565] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b233: Optional[B233] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b244: Optional[B244] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[ResourceidentifierRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ResourceidentifierShortname] = field(
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
