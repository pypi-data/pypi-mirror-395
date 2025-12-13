from dataclasses import dataclass, field
from typing import Optional

from .copyright_owner import CopyrightOwner
from .copyright_statement_refname import CopyrightStatementRefname
from .copyright_statement_shortname import CopyrightStatementShortname
from .copyright_type import CopyrightType
from .copyright_year import CopyrightYear
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class CopyrightStatement:
    """
    Details of a copyright or neighbouring rights statement ● Modified cardinality
    of &lt;CopyrightYear&gt; at revision 3.0.7 ● Added &lt;CopyrightType&gt; at
    revision 3.0.2.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    copyright_type: Optional[CopyrightType] = field(
        default=None,
        metadata={
            "name": "CopyrightType",
            "type": "Element",
        },
    )
    copyright_year: list[CopyrightYear] = field(
        default_factory=list,
        metadata={
            "name": "CopyrightYear",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    copyright_owner: list[CopyrightOwner] = field(
        default_factory=list,
        metadata={
            "name": "CopyrightOwner",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    refname: Optional[CopyrightStatementRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CopyrightStatementShortname] = field(
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
