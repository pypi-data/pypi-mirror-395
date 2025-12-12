from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .title_detail_refname import TitleDetailRefname
from .title_detail_shortname import TitleDetailShortname
from .title_element import TitleElement
from .title_statement import TitleStatement
from .title_type import TitleType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class TitleDetail:
    """
    Details of a title of a product (or a collection of products, or of a content
    item) ● Added &lt;TitleStatement&gt; at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    title_type: Optional[TitleType] = field(
        default=None,
        metadata={
            "name": "TitleType",
            "type": "Element",
            "required": True,
        },
    )
    title_element: list[TitleElement] = field(
        default_factory=list,
        metadata={
            "name": "TitleElement",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    title_statement: Optional[TitleStatement] = field(
        default=None,
        metadata={
            "name": "TitleStatement",
            "type": "Element",
        },
    )
    refname: Optional[TitleDetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TitleDetailShortname] = field(
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
