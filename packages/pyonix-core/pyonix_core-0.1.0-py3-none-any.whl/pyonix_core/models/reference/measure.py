from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .measure_refname import MeasureRefname
from .measure_shortname import MeasureShortname
from .measure_type import MeasureType
from .measure_unit_code import MeasureUnitCode
from .measurement import Measurement

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Measure:
    """
    Detail of a physical measurement – a dimension of the product.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    measure_type: Optional[MeasureType] = field(
        default=None,
        metadata={
            "name": "MeasureType",
            "type": "Element",
            "required": True,
        },
    )
    measurement: Optional[Measurement] = field(
        default=None,
        metadata={
            "name": "Measurement",
            "type": "Element",
            "required": True,
        },
    )
    measure_unit_code: Optional[MeasureUnitCode] = field(
        default=None,
        metadata={
            "name": "MeasureUnitCode",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[MeasureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[MeasureShortname] = field(
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
