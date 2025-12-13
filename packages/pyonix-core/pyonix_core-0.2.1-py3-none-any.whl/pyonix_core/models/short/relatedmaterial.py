from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .relatedmaterial_refname import RelatedmaterialRefname
from .relatedmaterial_shortname import RelatedmaterialShortname
from .relatedproduct import Relatedproduct
from .relatedwork import Relatedwork

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Relatedmaterial:
    """
    Block 5, container for elements providing links to closely-related products and
    works.
    """

    class Meta:
        name = "relatedmaterial"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    relatedwork: list[Relatedwork] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    relatedproduct: list[Relatedproduct] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[RelatedmaterialRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[RelatedmaterialShortname] = field(
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
