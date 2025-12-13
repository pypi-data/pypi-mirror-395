from dataclasses import dataclass, field
from typing import Optional

from .j349 import J349
from .j350 import J350
from .j351 import J351
from .j375 import J375
from .list3 import List3
from .locationidentifier import Locationidentifier
from .onorderdetail import Onorderdetail
from .stock_refname import StockRefname
from .stock_shortname import StockShortname
from .stockquantitycoded import Stockquantitycoded
from .velocity import Velocity
from .x502 import X502
from .x536 import X536

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Stock:
    """
    Details of a supplier’s stock holding ● Added &lt;Reserved&gt; and adjacent
    &lt;Proximity&gt; at revision 3.0.4 ● Modified cardinality of
    &lt;LocationIdentifier&gt;, &lt;LocationName&gt; at revision 3.0.3 ● Added
    &lt;Proximity&gt;, &lt;Velocity&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;StockQuantityCoded&gt; at revision 3.0.2.
    """

    class Meta:
        name = "stock"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    locationidentifier: list[Locationidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j349: list[J349] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    stockquantitycoded: list[Stockquantitycoded] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j350: Optional[J350] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x502: list[X502] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    x536: Optional[X536] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j351: Optional[J351] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j375: Optional[J375] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    onorderdetail: list[Onorderdetail] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    velocity: list[Velocity] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[StockRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[StockShortname] = field(
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
