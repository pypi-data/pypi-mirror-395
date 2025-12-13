from dataclasses import dataclass, field
from typing import Optional

from .ancillarycontent import Ancillarycontent
from .audience import Audience
from .audiencerange import Audiencerange
from .b012 import B012
from .b014 import B014
from .b049 import B049
from .b057 import B057
from .b058 import B058
from .b062 import B062
from .b063 import B063
from .b073 import B073
from .b125 import B125
from .b207 import B207
from .b217 import B217
from .b225 import B225
from .b333 import B333
from .b368 import B368
from .b369 import B369
from .b370 import B370
from .b384 import B384
from .b385 import B385
from .collection import Collection
from .complexity import Complexity
from .conference import Conference
from .contributor import Contributor
from .descriptivedetail_refname import DescriptivedetailRefname
from .descriptivedetail_shortname import DescriptivedetailShortname
from .epublicense import Epublicense
from .epubusageconstraint import Epubusageconstraint
from .event import Event
from .extent import Extent
from .language import Language
from .list3 import List3
from .measure import Measure
from .n339 import N339
from .n386 import N386
from .nameassubject import Nameassubject
from .productclassification import Productclassification
from .productformfeature import Productformfeature
from .productpart import Productpart
from .religioustext import Religioustext
from .subject import Subject
from .titledetail import Titledetail
from .x314 import X314
from .x316 import X316
from .x317 import X317
from .x411 import X411
from .x416 import X416
from .x419 import X419
from .x422 import X422

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Descriptivedetail:
    """
    Block 1, container for data describing the form and content of the product ●
    Added &lt;Event&gt;, deprecated &lt;Conference&gt; at revision 3.0.3 ● Added
    &lt;EpubLicence&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;ContributorStatement&gt;, &lt;EditionStatement&gt;,
    &lt;IllustrationsNote&gt;, &lt;AudienceDescription&gt; at revision 3.0.1.
    """

    class Meta:
        name = "descriptivedetail"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x314: Optional[X314] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b012: Optional[B012] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b333: list[B333] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    productformfeature: list[Productformfeature] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b225: Optional[B225] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b014: list[B014] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b384: Optional[B384] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x416: Optional[X416] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b385: list[B385] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    measure: list[Measure] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x316: Optional[X316] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x317: list[X317] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    epubusageconstraint: list[Epubusageconstraint] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    epublicense: Optional[Epublicense] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b063: list[B063] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    productclassification: list[Productclassification] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    productpart: list[Productpart] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    collection: list[Collection] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x411: Optional[X411] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    titledetail: list[Titledetail] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    b368: Optional[B368] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b369: Optional[B369] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b370: Optional[B370] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    contributor: list[Contributor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b049: list[B049] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    n339: Optional[N339] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    event: list[Event] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    conference: list[Conference] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x419: list[X419] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b057: Optional[B057] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b217: Optional[B217] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b058: list[B058] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    n386: Optional[N386] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    religioustext: Optional[Religioustext] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    language: list[Language] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    extent: list[Extent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x422: Optional[X422] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b125: Optional[B125] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b062: list[B062] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ancillarycontent: list[Ancillarycontent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    subject: list[Subject] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    nameassubject: list[Nameassubject] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b073: list[B073] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    audience: list[Audience] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    audiencerange: list[Audiencerange] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b207: list[B207] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    complexity: list[Complexity] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[DescriptivedetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[DescriptivedetailShortname] = field(
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
