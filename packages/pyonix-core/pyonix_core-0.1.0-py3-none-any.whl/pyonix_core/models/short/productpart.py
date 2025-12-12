from dataclasses import dataclass, field
from typing import Optional

from .b012 import B012
from .b014 import B014
from .b225 import B225
from .b333 import B333
from .b385 import B385
from .list3 import List3
from .measure import Measure
from .productformfeature import Productformfeature
from .productidentifier import Productidentifier
from .productpart_refname import ProductpartRefname
from .productpart_shortname import ProductpartShortname
from .x316 import X316
from .x322 import X322
from .x323 import X323
from .x457 import X457

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Productpart:
    """Details of a component which comprises part of the product.

    Note that components may also be product items in their own right ●
    Added &lt;Measure&gt; at revision 3.0.6 ● Added
    &lt;ProductPckaging&gt; at revision 3.0.3 ● Modified cardinality of
    &lt;ProductFormDescription&gt; at revision 3.0.1
    """

    class Meta:
        name = "productpart"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x457: Optional[X457] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    productidentifier: list[Productidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b012: Optional[B012] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b333: list[B333] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    productformfeature: list[Productformfeature] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b225: Optional[B225] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b014: list[B014] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    b385: list[B385] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    measure: list[Measure] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x322: Optional[X322] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    x323: list[X323] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    x316: Optional[X316] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ProductpartRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductpartShortname] = field(
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
