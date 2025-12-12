from dataclasses import dataclass, field
from typing import Optional

from .b358 import B358
from .b359 import B359
from .b360 import B360
from .list3 import List3
from .religioustextfeature_refname import ReligioustextfeatureRefname
from .religioustextfeature_shortname import ReligioustextfeatureShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Religioustextfeature:
    """
    ● Modified cardinality of &lt;ReligiousTextFeatureDescription&gt; at revision
    3.0.1.
    """

    class Meta:
        name = "religioustextfeature"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b358: Optional[B358] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b359: Optional[B359] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b360: list[B360] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ReligioustextfeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ReligioustextfeatureShortname] = field(
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
