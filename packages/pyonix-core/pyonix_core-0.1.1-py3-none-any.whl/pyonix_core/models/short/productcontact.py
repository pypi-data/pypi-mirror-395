from dataclasses import dataclass, field
from typing import Optional

from .j270 import J270
from .j272 import J272
from .list3 import List3
from .productcontact_refname import ProductcontactRefname
from .productcontact_shortname import ProductcontactShortname
from .productcontactidentifier import Productcontactidentifier
from .x299 import X299
from .x482 import X482
from .x484 import X484

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Productcontact:
    """
    Details of a organization responsible for answering enquiries about the product
    ● Added &lt;TelephoneNumber&gt; at 3.0.8 ● Added at revision 3.0.1.
    """

    class Meta:
        name = "productcontact"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x482: Optional[X482] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    productcontactidentifier: list[Productcontactidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    x484: list[X484] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    x299: Optional[X299] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j270: list[J270] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j272: Optional[J272] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ProductcontactRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductcontactShortname] = field(
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
