from dataclasses import dataclass, field
from typing import Optional

from .feature_note import FeatureNote
from .feature_value import FeatureValue
from .list3 import List3
from .resource_version_feature_refname import ResourceVersionFeatureRefname
from .resource_version_feature_shortname import ResourceVersionFeatureShortname
from .resource_version_feature_type import ResourceVersionFeatureType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ResourceVersionFeature:
    """
    Details of a particular feature of one version of a resource used for marketing
    and promotional purposes ● Modified cardinality of &lt;FeatureNote&gt; at
    revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    resource_version_feature_type: Optional[ResourceVersionFeatureType] = (
        field(
            default=None,
            metadata={
                "name": "ResourceVersionFeatureType",
                "type": "Element",
                "required": True,
            },
        )
    )
    feature_value: Optional[FeatureValue] = field(
        default=None,
        metadata={
            "name": "FeatureValue",
            "type": "Element",
        },
    )
    feature_note: list[FeatureNote] = field(
        default_factory=list,
        metadata={
            "name": "FeatureNote",
            "type": "Element",
        },
    )
    refname: Optional[ResourceVersionFeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ResourceVersionFeatureShortname] = field(
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
