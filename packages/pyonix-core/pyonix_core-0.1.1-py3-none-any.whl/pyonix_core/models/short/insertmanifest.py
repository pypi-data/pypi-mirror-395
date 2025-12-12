from dataclasses import dataclass, field
from typing import Optional

from .insertmanifest_refname import InsertmanifestRefname
from .insertmanifest_shortname import InsertmanifestShortname
from .insertpoint import Insertpoint
from .insertresource import Insertresource
from .list3 import List3
from .specificationbundlename import Specificationbundlename
from .specificationfeature import Specificationfeature
from .x560 import X560
from .x564 import X564

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Insertmanifest:
    """
    Details of the resource files needed to manufacture or package an insert ●
    Added at revision 3.0.8.
    """

    class Meta:
        name = "insertmanifest"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    specificationbundlename: list[Specificationbundlename] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x560: list[X560] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    specificationfeature: list[Specificationfeature] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x564: list[X564] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    insertpoint: Optional[Insertpoint] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    insertresource: list[Insertresource] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[InsertmanifestRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[InsertmanifestShortname] = field(
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
