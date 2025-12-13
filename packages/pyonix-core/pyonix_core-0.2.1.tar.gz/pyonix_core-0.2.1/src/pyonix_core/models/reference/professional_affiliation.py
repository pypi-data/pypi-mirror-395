from dataclasses import dataclass, field
from typing import Optional

from .affiliation import Affiliation
from .list3 import List3
from .professional_affiliation_refname import ProfessionalAffiliationRefname
from .professional_affiliation_shortname import (
    ProfessionalAffiliationShortname,
)
from .professional_position import ProfessionalPosition

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ProfessionalAffiliation:
    """
    Details of a professional position held by a contributor to the product at the
    time of its creation ● Modified cardinality of &lt;ProfessionalPosition&gt; at
    revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    professional_position: list[ProfessionalPosition] = field(
        default_factory=list,
        metadata={
            "name": "ProfessionalPosition",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    affiliation: list[Affiliation] = field(
        default_factory=list,
        metadata={
            "name": "Affiliation",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    refname: Optional[ProfessionalAffiliationRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProfessionalAffiliationShortname] = field(
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
