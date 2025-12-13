from dataclasses import dataclass, field
from typing import Optional

from .b306 import B306
from .j260 import J260
from .list3 import List3
from .supplydate_refname import SupplydateRefname
from .supplydate_shortname import SupplydateShortname
from .x461 import X461

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Supplydate:
    """
    Date of the specified role associated with the supply status of the product, eg
    expected ship date ● Modified cardinality of &lt;DateFormat&gt; at revision 3.0
    (2010)
    """

    class Meta:
        name = "supplydate"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x461: Optional[X461] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    j260: Optional[J260] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b306: Optional[B306] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[SupplydateRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SupplydateShortname] = field(
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
