from dataclasses import dataclass, field
from typing import Optional

from .b012 import B012
from .b333 import B333
from .list3 import List3
from .productidentifier import Productidentifier
from .relatedproduct_refname import RelatedproductRefname
from .relatedproduct_shortname import RelatedproductShortname
from .x455 import X455

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Relatedproduct:
    """
    Details of another product related in some way to the product ● Added
    &lt;ProductForm&gt;, &lt;ProductFormDetail&gt; at revision 3.0 (2010) ●
    Modified cardinality of &lt;ProductRelationCode&gt; at revision 3.0 (2010)
    """

    class Meta:
        name = "relatedproduct"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x455: list[X455] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    productidentifier: list[Productidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    b012: Optional[B012] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b333: list[B333] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[RelatedproductRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[RelatedproductShortname] = field(
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
