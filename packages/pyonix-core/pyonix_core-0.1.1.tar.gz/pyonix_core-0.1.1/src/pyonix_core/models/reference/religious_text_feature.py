from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .religious_text_feature_code import ReligiousTextFeatureCode
from .religious_text_feature_description import ReligiousTextFeatureDescription
from .religious_text_feature_refname import ReligiousTextFeatureRefname
from .religious_text_feature_shortname import ReligiousTextFeatureShortname
from .religious_text_feature_type import ReligiousTextFeatureType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ReligiousTextFeature:
    """
    ● Modified cardinality of &lt;ReligiousTextFeatureDescription&gt; at revision
    3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    religious_text_feature_type: Optional[ReligiousTextFeatureType] = field(
        default=None,
        metadata={
            "name": "ReligiousTextFeatureType",
            "type": "Element",
            "required": True,
        },
    )
    religious_text_feature_code: Optional[ReligiousTextFeatureCode] = field(
        default=None,
        metadata={
            "name": "ReligiousTextFeatureCode",
            "type": "Element",
            "required": True,
        },
    )
    religious_text_feature_description: list[
        ReligiousTextFeatureDescription
    ] = field(
        default_factory=list,
        metadata={
            "name": "ReligiousTextFeatureDescription",
            "type": "Element",
        },
    )
    refname: Optional[ReligiousTextFeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ReligiousTextFeatureShortname] = field(
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
