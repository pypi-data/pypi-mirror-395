from dataclasses import dataclass, field
from typing import Optional

from .addressee_refname import AddresseeRefname
from .addressee_shortname import AddresseeShortname
from .addresseeidentifier import Addresseeidentifier
from .j270 import J270
from .j272 import J272
from .list3 import List3
from .x299 import X299
from .x300 import X300

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Addressee:
    """
    Details of the intended recipient organization(s) for the ONIX message ● Added
    &lt;TelephoneNumber&gt; at 3.0.8.
    """

    class Meta:
        name = "addressee"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    addresseeidentifier: list[Addresseeidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    x300: list[X300] = field(
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
    j270: Optional[J270] = field(
        default=None,
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
