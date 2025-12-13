from dataclasses import dataclass, field
from typing import Optional

from .email_address import EmailAddress
from .fax_number import FaxNumber
from .list3 import List3
from .new_supplier_refname import NewSupplierRefname
from .new_supplier_shortname import NewSupplierShortname
from .supplier_identifier import SupplierIdentifier
from .supplier_name import SupplierName
from .telephone_number import TelephoneNumber

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class NewSupplier:
    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    supplier_identifier: list[SupplierIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "SupplierIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    supplier_name: list[SupplierName] = field(
        default_factory=list,
        metadata={
            "name": "SupplierName",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    telephone_number: list[TelephoneNumber] = field(
        default_factory=list,
        metadata={
            "name": "TelephoneNumber",
            "type": "Element",
        },
    )
    fax_number: list[FaxNumber] = field(
        default_factory=list,
        metadata={
            "name": "FaxNumber",
            "type": "Element",
        },
    )
    email_address: list[EmailAddress] = field(
        default_factory=list,
        metadata={
            "name": "EmailAddress",
            "type": "Element",
        },
    )
    refname: Optional[NewSupplierRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[NewSupplierShortname] = field(
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
