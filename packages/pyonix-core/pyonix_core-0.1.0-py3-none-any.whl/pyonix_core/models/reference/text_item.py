from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .number_of_pages import NumberOfPages
from .page_run import PageRun
from .text_item_identifier import TextItemIdentifier
from .text_item_refname import TextItemRefname
from .text_item_shortname import TextItemShortname
from .text_item_type import TextItemType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class TextItem:
    """
    Details of a textual content item (eg a chapter)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    text_item_type: Optional[TextItemType] = field(
        default=None,
        metadata={
            "name": "TextItemType",
            "type": "Element",
            "required": True,
        },
    )
    text_item_identifier: list[TextItemIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "TextItemIdentifier",
            "type": "Element",
        },
    )
    page_run: list[PageRun] = field(
        default_factory=list,
        metadata={
            "name": "PageRun",
            "type": "Element",
        },
    )
    number_of_pages: Optional[NumberOfPages] = field(
        default=None,
        metadata={
            "name": "NumberOfPages",
            "type": "Element",
        },
    )
    refname: Optional[TextItemRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TextItemShortname] = field(
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
