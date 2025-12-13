from dataclasses import dataclass, field
from typing import Optional

from .content_audience import ContentAudience
from .list3 import List3
from .resource_content_type import ResourceContentType
from .resource_feature import ResourceFeature
from .resource_mode import ResourceMode
from .resource_version import ResourceVersion
from .supporting_resource_refname import SupportingResourceRefname
from .supporting_resource_shortname import SupportingResourceShortname
from .territory import Territory

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SupportingResource:
    """
    Details of a supporting resource used for marketing and promotional purposes,
    eg a cover image, author photo, sample of the content ● Added &lt;Territory&gt;
    at revision 3.0.3.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    resource_content_type: Optional[ResourceContentType] = field(
        default=None,
        metadata={
            "name": "ResourceContentType",
            "type": "Element",
            "required": True,
        },
    )
    content_audience: list[ContentAudience] = field(
        default_factory=list,
        metadata={
            "name": "ContentAudience",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "name": "Territory",
            "type": "Element",
        },
    )
    resource_mode: Optional[ResourceMode] = field(
        default=None,
        metadata={
            "name": "ResourceMode",
            "type": "Element",
            "required": True,
        },
    )
    resource_feature: list[ResourceFeature] = field(
        default_factory=list,
        metadata={
            "name": "ResourceFeature",
            "type": "Element",
        },
    )
    resource_version: list[ResourceVersion] = field(
        default_factory=list,
        metadata={
            "name": "ResourceVersion",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[SupportingResourceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SupportingResourceShortname] = field(
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
