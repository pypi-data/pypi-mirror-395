from dataclasses import dataclass, field
from typing import Optional

from .c094 import C094
from .c095 import C095
from .list3 import List3
from .measure_refname import MeasureRefname
from .measure_shortname import MeasureShortname
from .x315 import X315

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Measure:
    """
    Detail of a physical measurement – a dimension of the product.
    """

    class Meta:
        name = "measure"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x315: Optional[X315] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    c094: Optional[C094] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    c095: Optional[C095] = field(
        default=None,
        metadata={
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
