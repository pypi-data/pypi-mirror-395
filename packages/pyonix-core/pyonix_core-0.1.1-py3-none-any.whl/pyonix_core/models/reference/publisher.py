from dataclasses import dataclass, field
from typing import Optional

from .funding import Funding
from .list3 import List3
from .publisher_identifier import PublisherIdentifier
from .publisher_name import PublisherName
from .publisher_refname import PublisherRefname
from .publisher_shortname import PublisherShortname
from .publishing_role import PublishingRole
from .website import Website

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Publisher:
    """
    Details of an organisation responsible for publishing the product ● Added
    &lt;Funding&gt; at revision 3.0.3.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    publishing_role: Optional[PublishingRole] = field(
        default=None,
        metadata={
            "name": "PublishingRole",
            "type": "Element",
            "required": True,
        },
    )
    publisher_identifier: list[PublisherIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "PublisherIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    publisher_name: list[PublisherName] = field(
        default_factory=list,
        metadata={
            "name": "PublisherName",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    funding: list[Funding] = field(
        default_factory=list,
        metadata={
            "name": "Funding",
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
    refname: Optional[PublisherRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PublisherShortname] = field(
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
