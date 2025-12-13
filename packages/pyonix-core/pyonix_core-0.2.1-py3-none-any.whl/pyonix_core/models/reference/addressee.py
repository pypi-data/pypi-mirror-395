from dataclasses import dataclass, field
from typing import Optional

from .addressee_identifier import AddresseeIdentifier
from .addressee_name import AddresseeName
from .addressee_refname import AddresseeRefname
from .addressee_shortname import AddresseeShortname
from .contact_name import ContactName
from .email_address import EmailAddress
from .list3 import List3
from .telephone_number import TelephoneNumber

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Addressee:
    """
    Details of the intended recipient organization(s) for the ONIX message ● Added
    &lt;TelephoneNumber&gt; at 3.0.8.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    addressee_identifier: list[AddresseeIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "AddresseeIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    addressee_name: list[AddresseeName] = field(
        default_factory=list,
        metadata={
            "name": "AddresseeName",
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
    telephone_number: Optional[TelephoneNumber] = field(
        default=None,
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
    refname: Optional[AddresseeRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[AddresseeShortname] = field(
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
