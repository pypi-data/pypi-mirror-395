from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .supplier_code_type import SupplierCodeType
from .supplier_code_type_name import SupplierCodeTypeName
from .supplier_code_value import SupplierCodeValue
from .supplier_own_coding_refname import SupplierOwnCodingRefname
from .supplier_own_coding_shortname import SupplierOwnCodingShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SupplierOwnCoding:
    """
    ● Added &lt;SupplierCodeTypeName&gt; at revison 3.0.2.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    supplier_code_type: Optional[SupplierCodeType] = field(
        default=None,
        metadata={
            "name": "SupplierCodeType",
            "type": "Element",
            "required": True,
        },
    )
    supplier_code_type_name: Optional[SupplierCodeTypeName] = field(
        default=None,
        metadata={
            "name": "SupplierCodeTypeName",
            "type": "Element",
        },
    )
    supplier_code_value: Optional[SupplierCodeValue] = field(
        default=None,
        metadata={
            "name": "SupplierCodeValue",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[SupplierOwnCodingRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SupplierOwnCodingShortname] = field(
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
