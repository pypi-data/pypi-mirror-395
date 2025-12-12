from dataclasses import dataclass, field
from typing import Optional

from .avitem import Avitem
from .cited_content import CitedContent
from .component_number import ComponentNumber
from .component_type_name import ComponentTypeName
from .content_item_refname import ContentItemRefname
from .content_item_shortname import ContentItemShortname
from .contributor import Contributor
from .contributor_statement import ContributorStatement
from .language import Language
from .level_sequence_number import LevelSequenceNumber
from .list3 import List3
from .name_as_subject import NameAsSubject
from .no_contributor import NoContributor
from .related_product import RelatedProduct
from .related_work import RelatedWork
from .subject import Subject
from .supporting_resource import SupportingResource
from .text_content import TextContent
from .text_item import TextItem
from .title_detail import TitleDetail

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ContentItem:
    """
    Details of a textual content item (eg a chapter) ● Added &lt;AVItem&gt; at
    revision 3.0.5 ● Added &lt;ContributorStatement&gt;, &lt;NoContributor&gt; (in
    gp.authorship), &lt;Language&gt; at revision 3.0.4 ● Added
    &lt;RelatedProduct&gt; at revision 3.0.3 ● Modified cardinality of
    &lt;ContributorStatement&gt; at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    level_sequence_number: Optional[LevelSequenceNumber] = field(
        default=None,
        metadata={
            "name": "LevelSequenceNumber",
            "type": "Element",
        },
    )
    text_item: Optional[TextItem] = field(
        default=None,
        metadata={
            "name": "TextItem",
            "type": "Element",
        },
    )
    avitem: Optional[Avitem] = field(
        default=None,
        metadata={
            "name": "AVItem",
            "type": "Element",
        },
    )
    component_type_name: Optional[ComponentTypeName] = field(
        default=None,
        metadata={
            "name": "ComponentTypeName",
            "type": "Element",
            "required": True,
        },
    )
    component_number: list[ComponentNumber] = field(
        default_factory=list,
        metadata={
            "name": "ComponentNumber",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    title_detail: list[TitleDetail] = field(
        default_factory=list,
        metadata={
            "name": "TitleDetail",
            "type": "Element",
        },
    )
    contributor: list[Contributor] = field(
        default_factory=list,
        metadata={
            "name": "Contributor",
            "type": "Element",
        },
    )
    contributor_statement: list[ContributorStatement] = field(
        default_factory=list,
        metadata={
            "name": "ContributorStatement",
            "type": "Element",
        },
    )
    no_contributor: Optional[NoContributor] = field(
        default=None,
        metadata={
            "name": "NoContributor",
            "type": "Element",
        },
    )
    language: list[Language] = field(
        default_factory=list,
        metadata={
            "name": "Language",
            "type": "Element",
        },
    )
    subject: list[Subject] = field(
        default_factory=list,
        metadata={
            "name": "Subject",
            "type": "Element",
        },
    )
    name_as_subject: list[NameAsSubject] = field(
        default_factory=list,
        metadata={
            "name": "NameAsSubject",
            "type": "Element",
        },
    )
    text_content: list[TextContent] = field(
        default_factory=list,
        metadata={
            "name": "TextContent",
            "type": "Element",
        },
    )
    cited_content: list[CitedContent] = field(
        default_factory=list,
        metadata={
            "name": "CitedContent",
            "type": "Element",
        },
    )
    supporting_resource: list[SupportingResource] = field(
        default_factory=list,
        metadata={
            "name": "SupportingResource",
            "type": "Element",
        },
    )
    related_work: list[RelatedWork] = field(
        default_factory=list,
        metadata={
            "name": "RelatedWork",
            "type": "Element",
        },
    )
    related_product: list[RelatedProduct] = field(
        default_factory=list,
        metadata={
            "name": "RelatedProduct",
            "type": "Element",
        },
    )
    refname: Optional[ContentItemRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ContentItemShortname] = field(
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
