from dataclasses import dataclass, field
from typing import Optional

from .contentdate import Contentdate
from .list3 import List3
from .resourceversion_refname import ResourceversionRefname
from .resourceversion_shortname import ResourceversionShortname
from .resourceversionfeature import Resourceversionfeature
from .x435 import X435
from .x441 import X441

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Resourceversion:
    """
    Details of a specific version of a supporting resource used for marketing and
    promotional purposes, eg when the resource is an audio extract, the mp3 version
    of that extract, and when the resource is an image, the 200-pixel JPEG version
    of that image.
    """

    class Meta:
        name = "resourceversion"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x441: Optional[X441] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    resourceversionfeature: list[Resourceversionfeature] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x435: list[X435] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    contentdate: list[Contentdate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ResourceversionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ResourceversionShortname] = field(
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
