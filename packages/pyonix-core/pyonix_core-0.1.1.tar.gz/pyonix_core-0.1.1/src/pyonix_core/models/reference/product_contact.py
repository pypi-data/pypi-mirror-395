from dataclasses import dataclass, field
from typing import Optional

from .contact_name import ContactName
from .email_address import EmailAddress
from .list3 import List3
from .product_contact_identifier import ProductContactIdentifier
from .product_contact_name import ProductContactName
from .product_contact_refname import ProductContactRefname
from .product_contact_role import ProductContactRole
from .product_contact_shortname import ProductContactShortname
from .telephone_number import TelephoneNumber

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ProductContact:
    """
    Details of a organization responsible for answering enquiries about the product
    ● Added &lt;TelephoneNumber&gt; at 3.0.8 ● Added at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    product_contact_role: Optional[ProductContactRole] = field(
        default=None,
        metadata={
            "name": "ProductContactRole",
            "type": "Element",
            "required": True,
        },
    )
    product_contact_identifier: list[ProductContactIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ProductContactIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    product_contact_name: list[ProductContactName] = field(
        default_factory=list,
        metadata={
            "name": "ProductContactName",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    contact_name: Optional[ContactName] = field(
        default=None,
        metadata={
            "name": "ContactName",
            "type": "Element",
        },
    )
    telephone_number: list[TelephoneNumber] = field(
        default_factory=list,
        metadata={
            "name": "TelephoneNumber",
            "type": "Element",
        },
    )
    email_address: Optional[EmailAddress] = field(
        default=None,
        metadata={
            "name": "EmailAddress",
            "type": "Element",
        },
    )
    refname: Optional[ProductContactRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductContactShortname] = field(
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
