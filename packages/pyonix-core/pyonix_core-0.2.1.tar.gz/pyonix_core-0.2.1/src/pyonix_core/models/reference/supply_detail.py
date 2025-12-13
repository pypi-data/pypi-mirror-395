from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .new_supplier import NewSupplier
from .order_quantity_minimum import OrderQuantityMinimum
from .order_quantity_multiple import OrderQuantityMultiple
from .order_time import OrderTime
from .pack_quantity import PackQuantity
from .pallet_quantity import PalletQuantity
from .price import Price
from .product_availability import ProductAvailability
from .reissue import Reissue
from .returns_conditions import ReturnsConditions
from .stock import Stock
from .supplier import Supplier
from .supplier_own_coding import SupplierOwnCoding
from .supply_contact import SupplyContact
from .supply_date import SupplyDate
from .supply_detail_refname import SupplyDetailRefname
from .supply_detail_shortname import SupplyDetailShortname
from .unpriced_item_type import UnpricedItemType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SupplyDetail:
    """
    Container for data specifying a supplier operating in a market, the
    availability of the product from that supplier, and supplier’s commercial terms
    including prices ● Added &lt;PalletQuantity&gt; at revision 3.0.5 ● Added
    &lt;SupplyContact&gt; at revision 3.0.4 ● Added &lt;OrderQuantityMinimum&gt;,
    &lt;OrderQuantityMultiple&gt; at revision 3.0.3 ● Modified cardinality of
    &lt;Supplier&gt; at revision 3.0 (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    supplier: Optional[Supplier] = field(
        default=None,
        metadata={
            "name": "Supplier",
            "type": "Element",
            "required": True,
        },
    )
    supply_contact: list[SupplyContact] = field(
        default_factory=list,
        metadata={
            "name": "SupplyContact",
            "type": "Element",
        },
    )
    supplier_own_coding: list[SupplierOwnCoding] = field(
        default_factory=list,
        metadata={
            "name": "SupplierOwnCoding",
            "type": "Element",
        },
    )
    returns_conditions: list[ReturnsConditions] = field(
        default_factory=list,
        metadata={
            "name": "ReturnsConditions",
            "type": "Element",
        },
    )
    product_availability: Optional[ProductAvailability] = field(
        default=None,
        metadata={
            "name": "ProductAvailability",
            "type": "Element",
            "required": True,
        },
    )
    supply_date: list[SupplyDate] = field(
        default_factory=list,
        metadata={
            "name": "SupplyDate",
            "type": "Element",
        },
    )
    order_time: Optional[OrderTime] = field(
        default=None,
        metadata={
            "name": "OrderTime",
            "type": "Element",
        },
    )
    new_supplier: Optional[NewSupplier] = field(
        default=None,
        metadata={
            "name": "NewSupplier",
            "type": "Element",
        },
    )
    stock: list[Stock] = field(
        default_factory=list,
        metadata={
            "name": "Stock",
            "type": "Element",
        },
    )
    pack_quantity: Optional[PackQuantity] = field(
        default=None,
        metadata={
            "name": "PackQuantity",
            "type": "Element",
        },
    )
    pallet_quantity: Optional[PalletQuantity] = field(
        default=None,
        metadata={
            "name": "PalletQuantity",
            "type": "Element",
        },
    )
    order_quantity_minimum: list[OrderQuantityMinimum] = field(
        default_factory=list,
        metadata={
            "name": "OrderQuantityMinimum",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    order_quantity_multiple: Optional[OrderQuantityMultiple] = field(
        default=None,
        metadata={
            "name": "OrderQuantityMultiple",
            "type": "Element",
        },
    )
    unpriced_item_type: Optional[UnpricedItemType] = field(
        default=None,
        metadata={
            "name": "UnpricedItemType",
            "type": "Element",
        },
    )
    price: list[Price] = field(
        default_factory=list,
        metadata={
            "name": "Price",
            "type": "Element",
        },
    )
    reissue: Optional[Reissue] = field(
        default=None,
        metadata={
            "name": "Reissue",
            "type": "Element",
        },
    )
    refname: Optional[SupplyDetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SupplyDetailShortname] = field(
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
