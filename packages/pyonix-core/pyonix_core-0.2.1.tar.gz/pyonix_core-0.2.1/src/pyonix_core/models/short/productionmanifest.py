from dataclasses import dataclass, field
from typing import Optional

from .bodymanifest import Bodymanifest
from .covermanifest import Covermanifest
from .insertmanifest import Insertmanifest
from .list3 import List3
from .productidentifier import Productidentifier
from .productionmanifest_refname import ProductionmanifestRefname
from .productionmanifest_shortname import ProductionmanifestShortname
from .supplementmanifest import Supplementmanifest

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Productionmanifest:
    """
    Container for a file manifest and manufacturing specification for a product or
    product part ● Added at revision 3.0.8.
    """

    class Meta:
        name = "productionmanifest"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    productidentifier: list[Productidentifier] = field(
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
            "required": True,
        },
    )
    insertmanifest: list[Insertmanifest] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supplementmanifest: list[Supplementmanifest] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ProductionmanifestRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductionmanifestShortname] = field(
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
