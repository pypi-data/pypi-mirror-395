from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .resourceversionfeature_refname import ResourceversionfeatureRefname
from .resourceversionfeature_shortname import ResourceversionfeatureShortname
from .x439 import X439
from .x440 import X440
from .x442 import X442

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Resourceversionfeature:
    """
    Details of a particular feature of one version of a resource used for marketing
    and promotional purposes ● Modified cardinality of &lt;FeatureNote&gt; at
    revision 3.0.1.
    """

    class Meta:
        name = "resourceversionfeature"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x442: Optional[X442] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x439: Optional[X439] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x440: list[X440] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ResourceversionfeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ResourceversionfeatureShortname] = field(
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
