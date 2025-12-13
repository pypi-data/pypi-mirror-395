from dataclasses import dataclass, field
from typing import Optional

from .content_audience import ContentAudience
from .contributor import Contributor
from .contributor_reference import ContributorReference
from .contributor_statement import ContributorStatement
from .event_description import EventDescription
from .event_identifier import EventIdentifier
from .event_name import EventName
from .event_occurrence import EventOccurrence
from .event_sponsor import EventSponsor
from .event_status import EventStatus
from .event_type import EventType
from .list3 import List3
from .no_contributor import NoContributor
from .promotional_event_refname import PromotionalEventRefname
from .promotional_event_shortname import PromotionalEventShortname
from .supporting_resource import SupportingResource
from .website import Website

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class PromotionalEvent:
    """
    Details of an event held to promote the product ● Added
    &lt;SupportingResource&gt; at revision 3.0.8 ● Added at revision 3.0.7.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    event_identifier: list[EventIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "EventIdentifier",
            "type": "Element",
        },
    )
    event_type: list[EventType] = field(
        default_factory=list,
        metadata={
            "name": "EventType",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    event_status: Optional[EventStatus] = field(
        default=None,
        metadata={
            "name": "EventStatus",
            "type": "Element",
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
    event_name: list[EventName] = field(
        default_factory=list,
        metadata={
            "name": "EventName",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    contributor_reference: list[ContributorReference] = field(
        default_factory=list,
        metadata={
            "name": "ContributorReference",
            "type": "Element",
        },
    )
    contributor: list[Contributor] = field(
        default_factory=list,
        metadata={
            "name": "Contributor",
            "type": "Element",
            "sequence": 1,
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
    event_description: list[EventDescription] = field(
        default_factory=list,
        metadata={
            "name": "EventDescription",
            "type": "Element",
        },
    )
    event_occurrence: list[EventOccurrence] = field(
        default_factory=list,
        metadata={
            "name": "EventOccurrence",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    supporting_resource: list[SupportingResource] = field(
        default_factory=list,
        metadata={
            "name": "SupportingResource",
            "type": "Element",
        },
    )
    event_sponsor: list[EventSponsor] = field(
        default_factory=list,
        metadata={
            "name": "EventSponsor",
            "type": "Element",
        },
    )
    website: list[Website] = field(
        default_factory=list,
        metadata={
            "name": "Website",
            "type": "Element",
        },
    )
    refname: Optional[PromotionalEventRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PromotionalEventShortname] = field(
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
