from dataclasses import dataclass, field
from typing import Optional

from .agent_identifier import AgentIdentifier
from .agent_name import AgentName
from .agent_role import AgentRole
from .email_address import EmailAddress
from .fax_number import FaxNumber
from .list3 import List3
from .publisher_representative_refname import PublisherRepresentativeRefname
from .publisher_representative_shortname import (
    PublisherRepresentativeShortname,
)
from .telephone_number import TelephoneNumber
from .website import Website

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class PublisherRepresentative:
    """
    Details of an organisation appointed by the publisher to act on its behalf in a
    specific market, eg a ‘local publisher’, sales agent etc.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    agent_role: Optional[AgentRole] = field(
        default=None,
        metadata={
            "name": "AgentRole",
            "type": "Element",
            "required": True,
        },
    )
    agent_identifier: list[AgentIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "AgentIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    agent_name: list[AgentName] = field(
        default_factory=list,
        metadata={
            "name": "AgentName",
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
    website: list[Website] = field(
        default_factory=list,
        metadata={
            "name": "Website",
            "type": "Element",
        },
    )
    refname: Optional[PublisherRepresentativeRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PublisherRepresentativeShortname] = field(
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
