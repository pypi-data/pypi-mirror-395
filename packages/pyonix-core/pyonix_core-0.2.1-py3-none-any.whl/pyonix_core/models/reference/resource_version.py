from dataclasses import dataclass, field
from typing import Optional

from .content_date import ContentDate
from .list3 import List3
from .resource_form import ResourceForm
from .resource_link import ResourceLink
from .resource_version_feature import ResourceVersionFeature
from .resource_version_refname import ResourceVersionRefname
from .resource_version_shortname import ResourceVersionShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ResourceVersion:
    """
    Details of a specific version of a supporting resource used for marketing and
    promotional purposes, eg when the resource is an audio extract, the mp3 version
    of that extract, and when the resource is an image, the 200-pixel JPEG version
    of that image.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    resource_form: Optional[ResourceForm] = field(
        default=None,
        metadata={
            "name": "ResourceForm",
            "type": "Element",
            "required": True,
        },
    )
    resource_version_feature: list[ResourceVersionFeature] = field(
        default_factory=list,
        metadata={
            "name": "ResourceVersionFeature",
            "type": "Element",
        },
    )
    resource_link: list[ResourceLink] = field(
        default_factory=list,
        metadata={
            "name": "ResourceLink",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    content_date: list[ContentDate] = field(
        default_factory=list,
        metadata={
            "name": "ContentDate",
            "type": "Element",
        },
    )
    refname: Optional[ResourceVersionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ResourceVersionShortname] = field(
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
