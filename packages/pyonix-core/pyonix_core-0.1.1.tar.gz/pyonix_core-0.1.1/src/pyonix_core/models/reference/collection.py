from dataclasses import dataclass, field
from typing import Optional

from .collection_identifier import CollectionIdentifier
from .collection_refname import CollectionRefname
from .collection_sequence import CollectionSequence
from .collection_shortname import CollectionShortname
from .collection_type import CollectionType
from .contributor import Contributor
from .contributor_statement import ContributorStatement
from .list3 import List3
from .no_contributor import NoContributor
from .source_name import SourceName
from .title_detail import TitleDetail

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


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
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    collection_type: Optional[CollectionType] = field(
        default=None,
        metadata={
            "name": "CollectionType",
            "type": "Element",
            "required": True,
        },
    )
    source_name: Optional[SourceName] = field(
        default=None,
        metadata={
            "name": "SourceName",
            "type": "Element",
        },
    )
    collection_identifier: list[CollectionIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "CollectionIdentifier",
            "type": "Element",
        },
    )
    collection_sequence: list[CollectionSequence] = field(
        default_factory=list,
        metadata={
            "name": "CollectionSequence",
            "type": "Element",
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
    sourcename_attribute: Optional[str] = field(
        default=None,
        metadata={
            "name": "sourcename",
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
