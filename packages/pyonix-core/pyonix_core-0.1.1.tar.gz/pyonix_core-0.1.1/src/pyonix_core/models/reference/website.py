from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .website_description import WebsiteDescription
from .website_link import WebsiteLink
from .website_refname import WebsiteRefname
from .website_role import WebsiteRole
from .website_shortname import WebsiteShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Website:
    """
    Details of a website related to the product, contributor, publisher, supplier
    etc ● Modified cardinality of &lt;WebsiteLink&gt; at revision 3.0.6 ● Modified
    cardinality of &lt;WebsiteDescription&gt; at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    website_role: Optional[WebsiteRole] = field(
        default=None,
        metadata={
            "name": "WebsiteRole",
            "type": "Element",
        },
    )
    website_description: list[WebsiteDescription] = field(
        default_factory=list,
        metadata={
            "name": "WebsiteDescription",
            "type": "Element",
        },
    )
    website_link: list[WebsiteLink] = field(
        default_factory=list,
        metadata={
            "name": "WebsiteLink",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[WebsiteRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[WebsiteShortname] = field(
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
