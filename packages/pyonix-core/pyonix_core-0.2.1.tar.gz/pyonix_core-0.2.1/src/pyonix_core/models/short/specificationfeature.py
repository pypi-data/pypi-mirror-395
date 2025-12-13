from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .specificationfeature_refname import SpecificationfeatureRefname
from .specificationfeature_shortname import SpecificationfeatureShortname
from .x561 import X561
from .x562 import X562
from .x563 import X563

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Specificationfeature:
    """
    ● Added at revision 3.0.8.
    """

    class Meta:
        name = "specificationfeature"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x561: Optional[X561] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x562: Optional[X562] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x563: list[X563] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[SpecificationfeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SpecificationfeatureShortname] = field(
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
