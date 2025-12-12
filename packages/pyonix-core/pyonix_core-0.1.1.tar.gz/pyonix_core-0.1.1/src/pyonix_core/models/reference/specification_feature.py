from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .specification_feature_description import SpecificationFeatureDescription
from .specification_feature_refname import SpecificationFeatureRefname
from .specification_feature_shortname import SpecificationFeatureShortname
from .specification_feature_type import SpecificationFeatureType
from .specification_feature_value import SpecificationFeatureValue

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SpecificationFeature:
    """
    ● Added at revision 3.0.8.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    specification_feature_type: Optional[SpecificationFeatureType] = field(
        default=None,
        metadata={
            "name": "SpecificationFeatureType",
            "type": "Element",
            "required": True,
        },
    )
    specification_feature_value: Optional[SpecificationFeatureValue] = field(
        default=None,
        metadata={
            "name": "SpecificationFeatureValue",
            "type": "Element",
        },
    )
    specification_feature_description: list[
        SpecificationFeatureDescription
    ] = field(
        default_factory=list,
        metadata={
            "name": "SpecificationFeatureDescription",
            "type": "Element",
        },
    )
    refname: Optional[SpecificationFeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SpecificationFeatureShortname] = field(
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
