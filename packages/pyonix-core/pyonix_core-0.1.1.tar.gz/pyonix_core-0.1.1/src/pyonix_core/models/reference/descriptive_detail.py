from dataclasses import dataclass, field
from typing import Optional

from .ancillary_content import AncillaryContent
from .audience import Audience
from .audience_code import AudienceCode
from .audience_description import AudienceDescription
from .audience_range import AudienceRange
from .collection import Collection
from .complexity import Complexity
from .conference import Conference
from .contributor import Contributor
from .contributor_statement import ContributorStatement
from .country_of_manufacture import CountryOfManufacture
from .descriptive_detail_refname import DescriptiveDetailRefname
from .descriptive_detail_shortname import DescriptiveDetailShortname
from .edition_number import EditionNumber
from .edition_statement import EditionStatement
from .edition_type import EditionType
from .edition_version_number import EditionVersionNumber
from .epub_license import EpubLicense
from .epub_technical_protection import EpubTechnicalProtection
from .epub_usage_constraint import EpubUsageConstraint
from .event import Event
from .extent import Extent
from .illustrated import Illustrated
from .illustrations_note import IllustrationsNote
from .language import Language
from .list3 import List3
from .map_scale import MapScale
from .measure import Measure
from .name_as_subject import NameAsSubject
from .no_collection import NoCollection
from .no_contributor import NoContributor
from .no_edition import NoEdition
from .number_of_illustrations import NumberOfIllustrations
from .primary_content_type import PrimaryContentType
from .product_classification import ProductClassification
from .product_composition import ProductComposition
from .product_content_type import ProductContentType
from .product_form import ProductForm
from .product_form_description import ProductFormDescription
from .product_form_detail import ProductFormDetail
from .product_form_feature import ProductFormFeature
from .product_packaging import ProductPackaging
from .product_part import ProductPart
from .religious_text import ReligiousText
from .subject import Subject
from .thesis_presented_to import ThesisPresentedTo
from .thesis_type import ThesisType
from .thesis_year import ThesisYear
from .title_detail import TitleDetail
from .trade_category import TradeCategory

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class DescriptiveDetail:
    """
    Block 1, container for data describing the form and content of the product ●
    Added &lt;Event&gt;, deprecated &lt;Conference&gt; at revision 3.0.3 ● Added
    &lt;EpubLicence&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;ContributorStatement&gt;, &lt;EditionStatement&gt;,
    &lt;IllustrationsNote&gt;, &lt;AudienceDescription&gt; at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    product_composition: Optional[ProductComposition] = field(
        default=None,
        metadata={
            "name": "ProductComposition",
            "type": "Element",
            "required": True,
        },
    )
    product_form: Optional[ProductForm] = field(
        default=None,
        metadata={
            "name": "ProductForm",
            "type": "Element",
            "required": True,
        },
    )
    product_form_detail: list[ProductFormDetail] = field(
        default_factory=list,
        metadata={
            "name": "ProductFormDetail",
            "type": "Element",
        },
    )
    product_form_feature: list[ProductFormFeature] = field(
        default_factory=list,
        metadata={
            "name": "ProductFormFeature",
            "type": "Element",
        },
    )
    product_packaging: Optional[ProductPackaging] = field(
        default=None,
        metadata={
            "name": "ProductPackaging",
            "type": "Element",
        },
    )
    product_form_description: list[ProductFormDescription] = field(
        default_factory=list,
        metadata={
            "name": "ProductFormDescription",
            "type": "Element",
        },
    )
    trade_category: Optional[TradeCategory] = field(
        default=None,
        metadata={
            "name": "TradeCategory",
            "type": "Element",
        },
    )
    primary_content_type: Optional[PrimaryContentType] = field(
        default=None,
        metadata={
            "name": "PrimaryContentType",
            "type": "Element",
        },
    )
    product_content_type: list[ProductContentType] = field(
        default_factory=list,
        metadata={
            "name": "ProductContentType",
            "type": "Element",
        },
    )
    measure: list[Measure] = field(
        default_factory=list,
        metadata={
            "name": "Measure",
            "type": "Element",
        },
    )
    country_of_manufacture: Optional[CountryOfManufacture] = field(
        default=None,
        metadata={
            "name": "CountryOfManufacture",
            "type": "Element",
        },
    )
    epub_technical_protection: list[EpubTechnicalProtection] = field(
        default_factory=list,
        metadata={
            "name": "EpubTechnicalProtection",
            "type": "Element",
        },
    )
    epub_usage_constraint: list[EpubUsageConstraint] = field(
        default_factory=list,
        metadata={
            "name": "EpubUsageConstraint",
            "type": "Element",
        },
    )
    epub_license: Optional[EpubLicense] = field(
        default=None,
        metadata={
            "name": "EpubLicense",
            "type": "Element",
        },
    )
    map_scale: list[MapScale] = field(
        default_factory=list,
        metadata={
            "name": "MapScale",
            "type": "Element",
        },
    )
    product_classification: list[ProductClassification] = field(
        default_factory=list,
        metadata={
            "name": "ProductClassification",
            "type": "Element",
        },
    )
    product_part: list[ProductPart] = field(
        default_factory=list,
        metadata={
            "name": "ProductPart",
            "type": "Element",
        },
    )
    collection: list[Collection] = field(
        default_factory=list,
        metadata={
            "name": "Collection",
            "type": "Element",
        },
    )
    no_collection: Optional[NoCollection] = field(
        default=None,
        metadata={
            "name": "NoCollection",
            "type": "Element",
        },
    )
    title_detail: list[TitleDetail] = field(
        default_factory=list,
        metadata={
            "name": "TitleDetail",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    thesis_type: Optional[ThesisType] = field(
        default=None,
        metadata={
            "name": "ThesisType",
            "type": "Element",
        },
    )
    thesis_presented_to: Optional[ThesisPresentedTo] = field(
        default=None,
        metadata={
            "name": "ThesisPresentedTo",
            "type": "Element",
        },
    )
    thesis_year: Optional[ThesisYear] = field(
        default=None,
        metadata={
            "name": "ThesisYear",
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
    event: list[Event] = field(
        default_factory=list,
        metadata={
            "name": "Event",
            "type": "Element",
        },
    )
    conference: list[Conference] = field(
        default_factory=list,
        metadata={
            "name": "Conference",
            "type": "Element",
        },
    )
    edition_type: list[EditionType] = field(
        default_factory=list,
        metadata={
            "name": "EditionType",
            "type": "Element",
        },
    )
    edition_number: Optional[EditionNumber] = field(
        default=None,
        metadata={
            "name": "EditionNumber",
            "type": "Element",
        },
    )
    edition_version_number: Optional[EditionVersionNumber] = field(
        default=None,
        metadata={
            "name": "EditionVersionNumber",
            "type": "Element",
        },
    )
    edition_statement: list[EditionStatement] = field(
        default_factory=list,
        metadata={
            "name": "EditionStatement",
            "type": "Element",
        },
    )
    no_edition: Optional[NoEdition] = field(
        default=None,
        metadata={
            "name": "NoEdition",
            "type": "Element",
        },
    )
    religious_text: Optional[ReligiousText] = field(
        default=None,
        metadata={
            "name": "ReligiousText",
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
    extent: list[Extent] = field(
        default_factory=list,
        metadata={
            "name": "Extent",
            "type": "Element",
        },
    )
    illustrated: Optional[Illustrated] = field(
        default=None,
        metadata={
            "name": "Illustrated",
            "type": "Element",
        },
    )
    number_of_illustrations: Optional[NumberOfIllustrations] = field(
        default=None,
        metadata={
            "name": "NumberOfIllustrations",
            "type": "Element",
        },
    )
    illustrations_note: list[IllustrationsNote] = field(
        default_factory=list,
        metadata={
            "name": "IllustrationsNote",
            "type": "Element",
        },
    )
    ancillary_content: list[AncillaryContent] = field(
        default_factory=list,
        metadata={
            "name": "AncillaryContent",
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
    audience_code: list[AudienceCode] = field(
        default_factory=list,
        metadata={
            "name": "AudienceCode",
            "type": "Element",
        },
    )
    audience: list[Audience] = field(
        default_factory=list,
        metadata={
            "name": "Audience",
            "type": "Element",
        },
    )
    audience_range: list[AudienceRange] = field(
        default_factory=list,
        metadata={
            "name": "AudienceRange",
            "type": "Element",
        },
    )
    audience_description: list[AudienceDescription] = field(
        default_factory=list,
        metadata={
            "name": "AudienceDescription",
            "type": "Element",
        },
    )
    complexity: list[Complexity] = field(
        default_factory=list,
        metadata={
            "name": "Complexity",
            "type": "Element",
        },
    )
    refname: Optional[DescriptiveDetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[DescriptiveDetailShortname] = field(
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
