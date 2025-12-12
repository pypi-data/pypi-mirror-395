from dataclasses import dataclass, field
from typing import Optional

from .b020 import B020
from .b029 import B029
from .b030 import B030
from .b031 import B031
from .b034 import B034
from .b203 import B203
from .list3 import List3
from .titleelement_refname import TitleelementRefname
from .titleelement_shortname import TitleelementShortname
from .x409 import X409
from .x410 import X410
from .x501 import X501

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Titleelement:
    """
    Details of one element (or part) of a title of a product, collection or content
    item ● Added &lt;NoPrefix&gt; at revision 3.0.2 ● Added &lt;SequenceNumber&gt;
    at revision 3.0.1.
    """

    class Meta:
        name = "titleelement"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b034: Optional[B034] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x409: Optional[X409] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x410: Optional[X410] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b020: list[B020] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 2,
        },
    )
    b030: list[B030] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 3,
        },
    )
    x501: list[X501] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 3,
        },
    )
    b031: list[B031] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 3,
        },
    )
    b203: list[B203] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 3,
        },
    )
    b029: Optional[B029] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[TitleelementRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TitleelementShortname] = field(
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
