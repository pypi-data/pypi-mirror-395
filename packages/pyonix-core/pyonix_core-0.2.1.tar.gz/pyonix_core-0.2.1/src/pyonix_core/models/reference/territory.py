from dataclasses import dataclass, field
from typing import Optional

from .countries_excluded import CountriesExcluded
from .countries_included import CountriesIncluded
from .list3 import List3
from .regions_excluded import RegionsExcluded
from .regions_included import RegionsIncluded
from .territory_refname import TerritoryRefname
from .territory_shortname import TerritoryShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Territory:
    """
    Geographical area, for example an area within which a particular type of sales
    rights or restrictions apply.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    countries_included: Optional[CountriesIncluded] = field(
        default=None,
        metadata={
            "name": "CountriesIncluded",
            "type": "Element",
            "required": True,
        },
    )
    regions_included: list[RegionsIncluded] = field(
        default_factory=list,
        metadata={
            "name": "RegionsIncluded",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    regions_excluded: list[RegionsExcluded] = field(
        default_factory=list,
        metadata={
            "name": "RegionsExcluded",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    countries_excluded: Optional[CountriesExcluded] = field(
        default=None,
        metadata={
            "name": "CountriesExcluded",
            "type": "Element",
        },
    )
    refname: Optional[TerritoryRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[TerritoryShortname] = field(
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
