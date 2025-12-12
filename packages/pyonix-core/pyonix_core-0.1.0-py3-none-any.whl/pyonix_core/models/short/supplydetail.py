from dataclasses import dataclass, field
from typing import Optional

from .j144 import J144
from .j145 import J145
from .j192 import J192
from .j396 import J396
from .list3 import List3
from .newsupplier import Newsupplier
from .price import Price
from .reissue import Reissue
from .returnsconditions import Returnsconditions
from .stock import Stock
from .supplier import Supplier
from .supplierowncoding import Supplierowncoding
from .supplycontact import Supplycontact
from .supplydate import Supplydate
from .supplydetail_refname import SupplydetailRefname
from .supplydetail_shortname import SupplydetailShortname
from .x532 import X532
from .x533 import X533
from .x545 import X545

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Supplydetail:
    """
    Container for data specifying a supplier operating in a market, the
    availability of the product from that supplier, and supplier’s commercial terms
    including prices ● Added &lt;PalletQuantity&gt; at revision 3.0.5 ● Added
    &lt;SupplyContact&gt; at revision 3.0.4 ● Added &lt;OrderQuantityMinimum&gt;,
    &lt;OrderQuantityMultiple&gt; at revision 3.0.3 ● Modified cardinality of
    &lt;Supplier&gt; at revision 3.0 (2010)
    """

    class Meta:
        name = "supplydetail"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    supplier: Optional[Supplier] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    supplycontact: list[Supplycontact] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supplierowncoding: list[Supplierowncoding] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    returnsconditions: list[Returnsconditions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j396: Optional[J396] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    supplydate: list[Supplydate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j144: Optional[J144] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    newsupplier: Optional[Newsupplier] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    stock: list[Stock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j145: Optional[J145] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x545: Optional[X545] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x532: list[X532] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 2,
        },
    )
    x533: Optional[X533] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j192: Optional[J192] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    price: list[Price] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    reissue: Optional[Reissue] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[SupplydetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SupplydetailShortname] = field(
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
