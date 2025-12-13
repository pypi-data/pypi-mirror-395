from dataclasses import dataclass, field
from typing import Optional

from .avitem import Avitem
from .b049 import B049
from .b284 import B284
from .b288 import B288
from .b289 import B289
from .citedcontent import Citedcontent
from .contentitem_refname import ContentitemRefname
from .contentitem_shortname import ContentitemShortname
from .contributor import Contributor
from .language import Language
from .list3 import List3
from .n339 import N339
from .nameassubject import Nameassubject
from .relatedproduct import Relatedproduct
from .relatedwork import Relatedwork
from .subject import Subject
from .supportingresource import Supportingresource
from .textcontent import Textcontent
from .textitem import Textitem
from .titledetail import Titledetail

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Contentitem:
    """
    Details of a textual content item (eg a chapter) ● Added &lt;AVItem&gt; at
    revision 3.0.5 ● Added &lt;ContributorStatement&gt;, &lt;NoContributor&gt; (in
    gp.authorship), &lt;Language&gt; at revision 3.0.4 ● Added
    &lt;RelatedProduct&gt; at revision 3.0.3 ● Modified cardinality of
    &lt;ContributorStatement&gt; at revision 3.0.1.
    """

    class Meta:
        name = "contentitem"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b284: Optional[B284] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    textitem: Optional[Textitem] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    avitem: Optional[Avitem] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b288: Optional[B288] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b289: list[B289] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 2,
        },
    )
    titledetail: list[Titledetail] = field(
        default_factory=list,
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
    language: list[Language] = field(
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
    textcontent: list[Textcontent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    citedcontent: list[Citedcontent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supportingresource: list[Supportingresource] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    relatedwork: list[Relatedwork] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    relatedproduct: list[Relatedproduct] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ContentitemRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ContentitemShortname] = field(
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
