from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .prize_code import PrizeCode
from .prize_country import PrizeCountry
from .prize_jury import PrizeJury
from .prize_name import PrizeName
from .prize_refname import PrizeRefname
from .prize_region import PrizeRegion
from .prize_shortname import PrizeShortname
from .prize_statement import PrizeStatement
from .prize_year import PrizeYear

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Prize:
    """
    Details of a literary or other prize associated with the product or work, or
    with a contributor ● Added &lt;PrizeRegion&gt; at revision 3.0.7 ● Added
    &lt;PrizeStatement&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;PrizeName&gt; at revision 3.0.2 ● Modified cardinality of &lt;PrizeJury&gt;
    at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    prize_name: list[PrizeName] = field(
        default_factory=list,
        metadata={
            "name": "PrizeName",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    prize_year: Optional[PrizeYear] = field(
        default=None,
        metadata={
            "name": "PrizeYear",
            "type": "Element",
        },
    )
    prize_country: Optional[PrizeCountry] = field(
        default=None,
        metadata={
            "name": "PrizeCountry",
            "type": "Element",
        },
    )
    prize_region: Optional[PrizeRegion] = field(
        default=None,
        metadata={
            "name": "PrizeRegion",
            "type": "Element",
        },
    )
    prize_code: Optional[PrizeCode] = field(
        default=None,
        metadata={
            "name": "PrizeCode",
            "type": "Element",
        },
    )
    prize_statement: list[PrizeStatement] = field(
        default_factory=list,
        metadata={
            "name": "PrizeStatement",
            "type": "Element",
        },
    )
    prize_jury: list[PrizeJury] = field(
        default_factory=list,
        metadata={
            "name": "PrizeJury",
            "type": "Element",
        },
    )
    refname: Optional[PrizeRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PrizeShortname] = field(
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
