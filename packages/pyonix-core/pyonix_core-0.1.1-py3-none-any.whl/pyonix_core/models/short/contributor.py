from dataclasses import dataclass, field
from typing import Optional

from .alternativename import Alternativename
from .b034 import B034
from .b035 import B035
from .b036 import B036
from .b037 import B037
from .b038 import B038
from .b039 import B039
from .b040 import B040
from .b041 import B041
from .b042 import B042
from .b043 import B043
from .b044 import B044
from .b047 import B047
from .b048 import B048
from .b247 import B247
from .b248 import B248
from .b249 import B249
from .contributor_refname import ContributorRefname
from .contributor_shortname import ContributorShortname
from .contributordate import Contributordate
from .contributorplace import Contributorplace
from .list3 import List3
from .nameidentifier import Nameidentifier
from .prize import Prize
from .professionalaffiliation import Professionalaffiliation
from .website import Website
from .x412 import X412
from .x413 import X413
from .x414 import X414
from .x443 import X443
from .x524 import X524

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Contributor:
    """
    Details of a person, persona or corporate identity – a contributor to the
    product (eg the author) ● Added &lt;Gender&gt;, &lt;Prize&gt; at revision 3.0.3
    ● Modified to allow &lt;NameIdentifier&gt; and &lt;AlternativeName&gt; with
    &lt;UnnamedPersons&gt; at revision 3.0.3 ● Modified cardinality of
    &lt;BiographicalNote&gt;, &lt;ContributorDescription&gt; at revision 3.0.1 ●
    Added &lt;CorporateNameInverted&gt; at revision 3.0 (2010)
    """

    class Meta:
        name = "contributor"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b034: Optional[B034] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b035: list[B035] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    x412: list[X412] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x413: list[X413] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x414: Optional[X414] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    nameidentifier: list[Nameidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    b036: list[B036] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 2,
        },
    )
    b037: list[B037] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b038: list[B038] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b039: list[B039] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b247: list[B247] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b040: list[B040] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b041: list[B041] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b248: list[B248] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b042: list[B042] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b043: list[B043] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    x524: list[X524] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b047: list[B047] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 2,
        },
    )
    x443: list[X443] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 4,
        },
    )
    b249: list[B249] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "max_occurs": 3,
        },
    )
    alternativename: list[Alternativename] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    contributordate: list[Contributordate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    professionalaffiliation: list[Professionalaffiliation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    prize: list[Prize] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b044: list[B044] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    website: list[Website] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b048: list[B048] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    contributorplace: list[Contributorplace] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ContributorRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ContributorShortname] = field(
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
