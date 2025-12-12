from dataclasses import dataclass, field
from typing import Optional

from .contributor_place_refname import ContributorPlaceRefname
from .contributor_place_relator import ContributorPlaceRelator
from .contributor_place_shortname import ContributorPlaceShortname
from .country_code import CountryCode
from .list3 import List3
from .location_name import LocationName
from .region_code import RegionCode

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ContributorPlace:
    """
    Location with which a contributor is associated ● Added &lt;LocationName&gt; at
    revision 3.0.2.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    contributor_place_relator: Optional[ContributorPlaceRelator] = field(
        default=None,
        metadata={
            "name": "ContributorPlaceRelator",
            "type": "Element",
            "required": True,
        },
    )
    country_code: Optional[CountryCode] = field(
        default=None,
        metadata={
            "name": "CountryCode",
            "type": "Element",
            "required": True,
        },
    )
    region_code: list[RegionCode] = field(
        default_factory=list,
        metadata={
            "name": "RegionCode",
            "type": "Element",
            "min_occurs": 1,
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
    refname: Optional[ContributorPlaceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ContributorPlaceShortname] = field(
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
