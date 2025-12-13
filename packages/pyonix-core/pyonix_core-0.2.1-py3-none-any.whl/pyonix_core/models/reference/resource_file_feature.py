from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .resource_file_feature_description import ResourceFileFeatureDescription
from .resource_file_feature_refname import ResourceFileFeatureRefname
from .resource_file_feature_shortname import ResourceFileFeatureShortname
from .resource_file_feature_type import ResourceFileFeatureType
from .resource_file_feature_value import ResourceFileFeatureValue

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ResourceFileFeature:
    """
    ● Added at revision 3.0.8.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    resource_file_feature_type: Optional[ResourceFileFeatureType] = field(
        default=None,
        metadata={
            "name": "ResourceFileFeatureType",
            "type": "Element",
            "required": True,
        },
    )
    resource_file_feature_value: Optional[ResourceFileFeatureValue] = field(
        default=None,
        metadata={
            "name": "ResourceFileFeatureValue",
            "type": "Element",
        },
    )
    resource_file_feature_description: list[ResourceFileFeatureDescription] = (
        field(
            default_factory=list,
            metadata={
                "name": "ResourceFileFeatureDescription",
                "type": "Element",
            },
        )
    )
    refname: Optional[ResourceFileFeatureRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ResourceFileFeatureShortname] = field(
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
