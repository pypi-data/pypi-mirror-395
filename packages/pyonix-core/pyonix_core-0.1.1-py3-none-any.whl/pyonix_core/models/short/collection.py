from dataclasses import dataclass, field
from typing import Optional

from .b049 import B049
from .collection_refname import CollectionRefname
from .collection_shortname import CollectionShortname
from .collectionidentifier import Collectionidentifier
from .collectionsequence import Collectionsequence
from .contributor import Contributor
from .list3 import List3
from .n339 import N339
from .titledetail import Titledetail
from .x329 import X329
from .x330 import X330

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Collection:
    """
    Details of a collection (eg a set or series, or a curated grouping of products)
    ● Added &lt;NoContributor&gt; (in gp.authorship) at revision 3.0.4 ● Added
    &lt;CollectionSequence&gt; and &lt;ContributorStatement&gt; (in gp.authorship)
    at revision 3.0.1 ● Modified cardinality of &lt;ContributorStatement&gt; at
    revision 3.0.1.
    """

    class Meta:
        name = "collection"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x329: Optional[X329] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x330: Optional[X330] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    collectionidentifier: list[Collectionidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    collectionsequence: list[Collectionsequence] = field(
        default_factory=list,
        metadata={
            "type": "Element",
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
    refname: Optional[CollectionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CollectionShortname] = field(
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
