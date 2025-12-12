from dataclasses import dataclass, field
from typing import Optional

from .b087 import B087
from .copyrightowner import Copyrightowner
from .copyrightstatement_refname import CopyrightstatementRefname
from .copyrightstatement_shortname import CopyrightstatementShortname
from .list3 import List3
from .x512 import X512

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Copyrightstatement:
    """
    Details of a copyright or neighbouring rights statement ● Modified cardinality
    of &lt;CopyrightYear&gt; at revision 3.0.7 ● Added &lt;CopyrightType&gt; at
    revision 3.0.2.
    """

    class Meta:
        name = "copyrightstatement"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x512: Optional[X512] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b087: list[B087] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    copyrightowner: list[Copyrightowner] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    refname: Optional[CopyrightstatementRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CopyrightstatementShortname] = field(
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
