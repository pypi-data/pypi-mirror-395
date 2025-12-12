from dataclasses import dataclass, field
from typing import Optional

from .epublicenseexpression_refname import EpublicenseexpressionRefname
from .epublicenseexpression_shortname import EpublicenseexpressionShortname
from .list3 import List3
from .x508 import X508
from .x509 import X509
from .x510 import X510

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Epublicenseexpression:
    """
    Details of a particular expression of an end user license ● Added at revision
    3.0.2.
    """

    class Meta:
        name = "epublicenseexpression"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x508: Optional[X508] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x509: Optional[X509] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x510: Optional[X510] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[EpublicenseexpressionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[EpublicenseexpressionShortname] = field(
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
