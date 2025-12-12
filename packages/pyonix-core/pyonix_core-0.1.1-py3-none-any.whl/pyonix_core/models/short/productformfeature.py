from dataclasses import dataclass, field
from typing import Optional

from .b334 import B334
from .b335 import B335
from .b336 import B336
from .list3 import List3
from .productformfeature_refname import ProductformfeatureRefname
from .productformfeature_shortname import ProductformfeatureShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Productformfeature:
    """Additional detail of the digital or physical nature of the product and its
    features, in addition to the &lt;ProductForm&gt; and &lt;ProductFormDetail&gt;.

    Repeatable if multiple different details are provided ● Modified
    cardinality of &lt;ProductFormFeatureDescription&gt; at revision
    3.0.1
    """

    class Meta:
        name = "productformfeature"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b334: Optional[B334] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b335: Optional[B335] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b336: list[B336] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[ProductformfeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductformfeatureShortname] = field(
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
