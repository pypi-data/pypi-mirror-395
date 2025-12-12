from dataclasses import dataclass, field
from typing import Optional

from .complexity_code import ComplexityCode
from .complexity_refname import ComplexityRefname
from .complexity_scheme_identifier import ComplexitySchemeIdentifier
from .complexity_shortname import ComplexityShortname
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Complexity:
    """
    Details of the difficulty of comprehension of the content.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    complexity_scheme_identifier: Optional[ComplexitySchemeIdentifier] = field(
        default=None,
        metadata={
            "name": "ComplexitySchemeIdentifier",
            "type": "Element",
            "required": True,
        },
    )
    complexity_code: Optional[ComplexityCode] = field(
        default=None,
        metadata={
            "name": "ComplexityCode",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[ComplexityRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ComplexityShortname] = field(
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
