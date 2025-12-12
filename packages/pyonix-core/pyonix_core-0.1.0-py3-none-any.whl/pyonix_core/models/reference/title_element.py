from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .no_prefix import NoPrefix
from .part_number import PartNumber
from .sequence_number import SequenceNumber
from .subtitle import Subtitle
from .title_element_level import TitleElementLevel
from .title_element_refname import TitleElementRefname
from .title_element_shortname import TitleElementShortname
from .title_prefix import TitlePrefix
from .title_text import TitleText
from .title_without_prefix import TitleWithoutPrefix
from .year_of_annual import YearOfAnnual

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class TitleElement:
    """
    Details of one element (or part) of a title of a product, collection or content
    item ● Added &lt;NoPrefix&gt; at revision 3.0.2 ● Added &lt;SequenceNumber&gt;
    at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sequence_number: Optional[SequenceNumber] = field(
        default=None,
        metadata={
            "name": "SequenceNumber",
            "type": "Element",
        },
    )
    title_element_level: Optional[TitleElementLevel] = field(
        default=None,
        metadata={
            "name": "TitleElementLevel",
            "type": "Element",
            "required": True,
        },
    )
    part_number: Optional[PartNumber] = field(
        default=None,
        metadata={
            "name": "PartNumber",
            "type": "Element",
            "required": True,
        },
    )
    year_of_annual: list[YearOfAnnual] = field(
        default_factory=list,
        metadata={
            "name": "YearOfAnnual",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    title_prefix: list[TitlePrefix] = field(
        default_factory=list,
        metadata={
            "name": "TitlePrefix",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    no_prefix: list[NoPrefix] = field(
        default_factory=list,
        metadata={
            "name": "NoPrefix",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    title_without_prefix: list[TitleWithoutPrefix] = field(
        default_factory=list,
        metadata={
            "name": "TitleWithoutPrefix",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    title_text: list[TitleText] = field(
        default_factory=list,
        metadata={
            "name": "TitleText",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    subtitle: Optional[Subtitle] = field(
        default=None,
        metadata={
            "name": "Subtitle",
            "type": "Element",
        },
    )
    refname: Optional[TitleElementRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TitleElementShortname] = field(
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
