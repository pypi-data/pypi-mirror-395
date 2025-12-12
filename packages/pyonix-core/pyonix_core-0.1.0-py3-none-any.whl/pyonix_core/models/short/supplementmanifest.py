from dataclasses import dataclass, field
from typing import Optional

from .b012 import B012
from .b014 import B014
from .b034 import B034
from .b333 import B333
from .bodymanifest import Bodymanifest
from .covermanifest import Covermanifest
from .insertmanifest import Insertmanifest
from .list3 import List3
from .measure import Measure
from .productidentifier import Productidentifier
from .salesoutlet import Salesoutlet
from .supplementmanifest_refname import SupplementmanifestRefname
from .supplementmanifest_shortname import SupplementmanifestShortname
from .x579 import X579

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Supplementmanifest:
    """
    Details of the resource files needed to manufacture or package a supplement to
    a product ● Added at revision 3.0.8.
    """

    class Meta:
        name = "supplementmanifest"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b034: Optional[B034] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    salesoutlet: list[Salesoutlet] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    productidentifier: list[Productidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b012: Optional[B012] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b333: list[B333] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b014: list[B014] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    measure: list[Measure] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    covermanifest: Optional[Covermanifest] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    bodymanifest: Optional[Bodymanifest] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    insertmanifest: list[Insertmanifest] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x579: Optional[X579] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[SupplementmanifestRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SupplementmanifestShortname] = field(
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
