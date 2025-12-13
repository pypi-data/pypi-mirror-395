from dataclasses import dataclass, field
from typing import Optional

from .b202 import B202
from .list3 import List3
from .titledetail_refname import TitledetailRefname
from .titledetail_shortname import TitledetailShortname
from .titleelement import Titleelement
from .x478 import X478

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Titledetail:
    """
    Details of a title of a product (or a collection of products, or of a content
    item) ● Added &lt;TitleStatement&gt; at revision 3.0.1.
    """

    class Meta:
        name = "titledetail"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b202: Optional[B202] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    titleelement: list[Titleelement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    x478: Optional[X478] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[TitledetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TitledetailShortname] = field(
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
