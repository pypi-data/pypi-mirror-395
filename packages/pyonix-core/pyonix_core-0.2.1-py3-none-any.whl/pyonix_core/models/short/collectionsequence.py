from dataclasses import dataclass, field
from typing import Optional

from .collectionsequence_refname import CollectionsequenceRefname
from .collectionsequence_shortname import CollectionsequenceShortname
from .list3 import List3
from .x479 import X479
from .x480 import X480
from .x481 import X481

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Collectionsequence:
    """
    Details of a product’s sequential position in a collection ● Added at revision
    3.0.1.
    """

    class Meta:
        name = "collectionsequence"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x479: Optional[X479] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x480: Optional[X480] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x481: Optional[X481] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[CollectionsequenceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CollectionsequenceShortname] = field(
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
