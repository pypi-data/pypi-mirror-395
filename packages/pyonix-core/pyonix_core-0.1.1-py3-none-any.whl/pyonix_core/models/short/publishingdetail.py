from dataclasses import dataclass, field
from typing import Optional

from .b083 import B083
from .b209 import B209
from .b394 import B394
from .b395 import B395
from .copyrightstatement import Copyrightstatement
from .imprint import Imprint
from .list3 import List3
from .productcontact import Productcontact
from .publisher import Publisher
from .publishingdate import Publishingdate
from .publishingdetail_refname import PublishingdetailRefname
from .publishingdetail_shortname import PublishingdetailShortname
from .salesrestriction import Salesrestriction
from .salesrights import Salesrights
from .x446 import X446
from .x456 import X456

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Publishingdetail:
    """
    Block 4, container for information about describing branding, publishing and
    rights attached to the product ● Added &lt;ProductContact&gt; at revision 3.0.1
    ● Modified cardinality of &lt;PublishingStatusNote&gt; at revision 3.0.1 ●
    Added &lt;ROWSalesRightsType&gt; at revision 3.0 (2010)
    """

    class Meta:
        name = "publishingdetail"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    imprint: list[Imprint] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    publisher: list[Publisher] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    b209: list[B209] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b083: Optional[B083] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    productcontact: list[Productcontact] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b394: Optional[B394] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b395: list[B395] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    publishingdate: list[Publishingdate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x446: Optional[X446] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    copyrightstatement: list[Copyrightstatement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    salesrights: list[Salesrights] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x456: Optional[X456] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    salesrestriction: list[Salesrestriction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[PublishingdetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PublishingdetailShortname] = field(
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
