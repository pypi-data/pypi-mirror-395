from dataclasses import dataclass, field
from typing import Optional

from .ancillarycontent_refname import AncillarycontentRefname
from .ancillarycontent_shortname import AncillarycontentShortname
from .b257 import B257
from .list3 import List3
from .x423 import X423
from .x424 import X424

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Ancillarycontent:
    """
    Details of illustrations, maps, table of contents, index, bibliography or other
    ancillary content ● Modified cardinality of &lt;AncillaryContentDescription&gt;
    at revision 3.0.1.
    """

    class Meta:
        name = "ancillarycontent"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x423: Optional[X423] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x424: list[X424] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b257: Optional[B257] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[AncillarycontentRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[AncillarycontentShortname] = field(
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
