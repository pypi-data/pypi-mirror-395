from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .price_part_description import PricePartDescription
from .product_identifier import ProductIdentifier
from .tax_amount import TaxAmount
from .tax_rate_code import TaxRateCode
from .tax_rate_percent import TaxRatePercent
from .tax_refname import TaxRefname
from .tax_shortname import TaxShortname
from .tax_type import TaxType
from .taxable_amount import TaxableAmount

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Tax:
    """
    Details of the type and amount of tax included within a Price amount ● Added
    &lt;PricePartDescription&gt; at revision 3.0.4 ● Added
    &lt;ProductIdentifier&gt; at revision 3.0.3.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    product_identifier: list[ProductIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ProductIdentifier",
            "type": "Element",
        },
    )
    price_part_description: list[PricePartDescription] = field(
        default_factory=list,
        metadata={
            "name": "PricePartDescription",
            "type": "Element",
        },
    )
    tax_type: Optional[TaxType] = field(
        default=None,
        metadata={
            "name": "TaxType",
            "type": "Element",
        },
    )
    tax_rate_code: Optional[TaxRateCode] = field(
        default=None,
        metadata={
            "name": "TaxRateCode",
            "type": "Element",
        },
    )
    tax_rate_percent: Optional[TaxRatePercent] = field(
        default=None,
        metadata={
            "name": "TaxRatePercent",
            "type": "Element",
            "required": True,
        },
    )
    taxable_amount: list[TaxableAmount] = field(
        default_factory=list,
        metadata={
            "name": "TaxableAmount",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    tax_amount: list[TaxAmount] = field(
        default_factory=list,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    refname: Optional[TaxRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TaxShortname] = field(
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
