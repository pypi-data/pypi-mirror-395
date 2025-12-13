from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .price import Price
from .reissue_date import ReissueDate
from .reissue_description import ReissueDescription
from .reissue_refname import ReissueRefname
from .reissue_shortname import ReissueShortname
from .supporting_resource import SupportingResource

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Reissue:
    """
    Details of a planned reissue of a product ● Deprecated – use start and end
    dates in &lt;Price&gt;, &lt;TextContent&gt;, &lt;SupportingResource&gt; etc
    instead.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    reissue_date: Optional[ReissueDate] = field(
        default=None,
        metadata={
            "name": "ReissueDate",
            "type": "Element",
            "required": True,
        },
    )
    reissue_description: Optional[ReissueDescription] = field(
        default=None,
        metadata={
            "name": "ReissueDescription",
            "type": "Element",
        },
    )
    price: list[Price] = field(
        default_factory=list,
        metadata={
            "name": "Price",
            "type": "Element",
        },
    )
    supporting_resource: list[SupportingResource] = field(
        default_factory=list,
        metadata={
            "name": "SupportingResource",
            "type": "Element",
        },
    )
    refname: Optional[ReissueRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ReissueShortname] = field(
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
