from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .returns_code import ReturnsCode
from .returns_code_type import ReturnsCodeType
from .returns_code_type_name import ReturnsCodeTypeName
from .returns_conditions_refname import ReturnsConditionsRefname
from .returns_conditions_shortname import ReturnsConditionsShortname
from .returns_note import ReturnsNote

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ReturnsConditions:
    """
    Details of the supplier’s returns conditions ● Added &lt;ReturnsNote&gt; at
    revision 3.0.3.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    returns_code_type: Optional[ReturnsCodeType] = field(
        default=None,
        metadata={
            "name": "ReturnsCodeType",
            "type": "Element",
            "required": True,
        },
    )
    returns_code_type_name: Optional[ReturnsCodeTypeName] = field(
        default=None,
        metadata={
            "name": "ReturnsCodeTypeName",
            "type": "Element",
        },
    )
    returns_code: Optional[ReturnsCode] = field(
        default=None,
        metadata={
            "name": "ReturnsCode",
            "type": "Element",
            "required": True,
        },
    )
    returns_note: list[ReturnsNote] = field(
        default_factory=list,
        metadata={
            "name": "ReturnsNote",
            "type": "Element",
        },
    )
    refname: Optional[ReturnsConditionsRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ReturnsConditionsShortname] = field(
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
