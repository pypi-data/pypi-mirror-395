from dataclasses import dataclass, field
from typing import Optional

from .content_audience import ContentAudience
from .content_date import ContentDate
from .list3 import List3
from .review_rating import ReviewRating
from .source_title import SourceTitle
from .territory import Territory
from .text import Text
from .text_author import TextAuthor
from .text_content_refname import TextContentRefname
from .text_content_shortname import TextContentShortname
from .text_source_corporate import TextSourceCorporate
from .text_source_description import TextSourceDescription
from .text_type import TextType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class TextContent:
    """
    Details of a supporting text, primarily for marketing and promotional purposes
    ● Added &lt;TextSourceDescription&gt; at revision 3.0.7 ● Added
    &lt;Territory&gt;, &lt;ReviewRating&gt; at revision 3.0.3 ● Modified
    cardinality of &lt;SourceTitle&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;Text&gt; at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    text_type: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "TextType",
            "type": "Element",
            "required": True,
        },
    )
    content_audience: list[ContentAudience] = field(
        default_factory=list,
        metadata={
            "name": "ContentAudience",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "name": "Territory",
            "type": "Element",
        },
    )
    text: list[Text] = field(
        default_factory=list,
        metadata={
            "name": "Text",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    review_rating: Optional[ReviewRating] = field(
        default=None,
        metadata={
            "name": "ReviewRating",
            "type": "Element",
        },
    )
    text_author: list[TextAuthor] = field(
        default_factory=list,
        metadata={
            "name": "TextAuthor",
            "type": "Element",
        },
    )
    text_source_corporate: Optional[TextSourceCorporate] = field(
        default=None,
        metadata={
            "name": "TextSourceCorporate",
            "type": "Element",
        },
    )
    text_source_description: list[TextSourceDescription] = field(
        default_factory=list,
        metadata={
            "name": "TextSourceDescription",
            "type": "Element",
        },
    )
    source_title: list[SourceTitle] = field(
        default_factory=list,
        metadata={
            "name": "SourceTitle",
            "type": "Element",
        },
    )
    content_date: list[ContentDate] = field(
        default_factory=list,
        metadata={
            "name": "ContentDate",
            "type": "Element",
        },
    )
    refname: Optional[TextContentRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TextContentShortname] = field(
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
