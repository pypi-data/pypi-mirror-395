from dataclasses import dataclass, field
from typing import Optional

from .covermanifest_refname import CovermanifestRefname
from .covermanifest_shortname import CovermanifestShortname
from .coverresource import Coverresource
from .list3 import List3
from .specificationbundlename import Specificationbundlename
from .specificationfeature import Specificationfeature
from .x560 import X560
from .x564 import X564

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Covermanifest:
    """
    Details of the resource files needed to manufacture or package the cover of a
    product ● Added at revision 3.0.8.
    """

    class Meta:
        name = "covermanifest"
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
    coverresource: list[Coverresource] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[CovermanifestRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CovermanifestShortname] = field(
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
