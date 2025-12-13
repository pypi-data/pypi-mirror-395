from dataclasses import dataclass, field
from typing import Optional

from .b274 import B274
from .b275 import B275
from .b337 import B337
from .list3 import List3
from .productclassification_refname import ProductclassificationRefname
from .productclassification_shortname import ProductclassificationShortname
from .x555 import X555

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Productclassification:
    """
    Details of a national or international trade classification (eg HMRC customs
    code, TARIC code, Schedule B code) ● Added
    &lt;ProductClassificationTypeName&gt; at revision 3.0.7.
    """

    class Meta:
        name = "productclassification"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b274: Optional[B274] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x555: Optional[X555] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b275: Optional[B275] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b337: Optional[B337] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ProductclassificationRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductclassificationShortname] = field(
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
