from dataclasses import dataclass, field
from typing import Optional

from .citation_note import CitationNote
from .cited_content_refname import CitedContentRefname
from .cited_content_shortname import CitedContentShortname
from .cited_content_type import CitedContentType
from .content_audience import ContentAudience
from .content_date import ContentDate
from .list3 import List3
from .list_name import ListName
from .position_on_list import PositionOnList
from .resource_link import ResourceLink
from .review_rating import ReviewRating
from .source_title import SourceTitle
from .source_type import SourceType
from .territory import Territory

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class CitedContent:
    """
    Third-party material which may be cited primarily for marketing and promotional
    purposes ● Added &lt;Territory&gt;, &lt;ReviewRating&gt; at revision 3.0.3 ●
    Modified cardinality of &lt;ListName&gt;, &lt;SourceTitle&gt; at revision 3.0.2
    ● Modified cardinality of &lt;CitationNote&gt; at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    cited_content_type: Optional[CitedContentType] = field(
        default=None,
        metadata={
            "name": "CitedContentType",
            "type": "Element",
            "required": True,
        },
    )
    content_audience: list[ContentAudience] = field(
        default_factory=list,
        metadata={
            "name": "ContentAudience",
            "type": "Element",
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "name": "Territory",
            "type": "Element",
        },
    )
    source_type: Optional[SourceType] = field(
        default=None,
        metadata={
            "name": "SourceType",
            "type": "Element",
        },
    )
    review_rating: Optional[ReviewRating] = field(
        default=None,
        metadata={
            "name": "ReviewRating",
            "type": "Element",
            "required": True,
        },
    )
    source_title: list[SourceTitle] = field(
        default_factory=list,
        metadata={
            "name": "SourceTitle",
            "type": "Element",
            "min_occurs": 2,
            "sequence": 1,
        },
    )
    list_name: list[ListName] = field(
        default_factory=list,
        metadata={
            "name": "ListName",
            "type": "Element",
        },
    )
    position_on_list: list[PositionOnList] = field(
        default_factory=list,
        metadata={
            "name": "PositionOnList",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    citation_note: list[CitationNote] = field(
        default_factory=list,
        metadata={
            "name": "CitationNote",
            "type": "Element",
        },
    )
    resource_link: list[ResourceLink] = field(
        default_factory=list,
        metadata={
            "name": "ResourceLink",
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
    refname: Optional[CitedContentRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CitedContentShortname] = field(
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
    sourcetype_attribute: Optional[List3] = field(
        default=None,
        metadata={
            "name": "sourcetype",
            "type": "Attribute",
        },
    )
