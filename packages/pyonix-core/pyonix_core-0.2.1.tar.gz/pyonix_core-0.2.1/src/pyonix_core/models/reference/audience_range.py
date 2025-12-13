from dataclasses import dataclass, field
from typing import Optional

from .audience_range_precision import AudienceRangePrecision
from .audience_range_qualifier import AudienceRangeQualifier
from .audience_range_refname import AudienceRangeRefname
from .audience_range_shortname import AudienceRangeShortname
from .audience_range_value import AudienceRangeValue
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class AudienceRange:
    """
    Details of a target audience range (by reading age, interest age, school year
    etc)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    audience_range_qualifier: Optional[AudienceRangeQualifier] = field(
        default=None,
        metadata={
            "name": "AudienceRangeQualifier",
            "type": "Element",
            "required": True,
        },
    )
    audience_range_precision: list[AudienceRangePrecision] = field(
        default_factory=list,
        metadata={
            "name": "AudienceRangePrecision",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    audience_range_value: list[AudienceRangeValue] = field(
        default_factory=list,
        metadata={
            "name": "AudienceRangeValue",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    refname: Optional[AudienceRangeRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[AudienceRangeShortname] = field(
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
