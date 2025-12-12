from dataclasses import dataclass, field
from typing import Optional

from .country_code import CountryCode
from .event_description import EventDescription
from .event_identifier import EventIdentifier
from .event_occurrence_refname import EventOccurrenceRefname
from .event_occurrence_shortname import EventOccurrenceShortname
from .event_sponsor import EventSponsor
from .event_status import EventStatus
from .list3 import List3
from .location_name import LocationName
from .occurrence_date import OccurrenceDate
from .region_code import RegionCode
from .street_address import StreetAddress
from .supporting_resource import SupportingResource
from .venue_name import VenueName
from .venue_note import VenueNote
from .website import Website

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class EventOccurrence:
    """
    Details for a particular occurrence of a promotional event ● Added
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
    occurrence_date: list[OccurrenceDate] = field(
        default_factory=list,
        metadata={
            "name": "OccurrenceDate",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    event_status: Optional[EventStatus] = field(
        default=None,
        metadata={
            "name": "EventStatus",
            "type": "Element",
            "required": True,
        },
    )
    country_code: Optional[CountryCode] = field(
        default=None,
        metadata={
            "name": "CountryCode",
            "type": "Element",
        },
    )
    region_code: list[RegionCode] = field(
        default_factory=list,
        metadata={
            "name": "RegionCode",
            "type": "Element",
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    location_name: list[LocationName] = field(
        default_factory=list,
        metadata={
            "name": "LocationName",
            "type": "Element",
        },
    )
    venue_name: Optional[VenueName] = field(
        default=None,
        metadata={
            "name": "VenueName",
            "type": "Element",
        },
    )
    street_address: Optional[StreetAddress] = field(
        default=None,
        metadata={
            "name": "StreetAddress",
            "type": "Element",
        },
    )
    venue_note: list[VenueNote] = field(
        default_factory=list,
        metadata={
            "name": "VenueNote",
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
    refname: Optional[EventOccurrenceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[EventOccurrenceShortname] = field(
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
