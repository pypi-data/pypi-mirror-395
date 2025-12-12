from dataclasses import dataclass, field
from typing import Optional

from .body_resource_refname import BodyResourceRefname
from .body_resource_shortname import BodyResourceShortname
from .list3 import List3
from .resource_file_content_description import ResourceFileContentDescription
from .resource_file_date import ResourceFileDate
from .resource_file_description import ResourceFileDescription
from .resource_file_detail import ResourceFileDetail
from .resource_file_feature import ResourceFileFeature
from .resource_file_link import ResourceFileLink
from .resource_identifier import ResourceIdentifier
from .resource_role import ResourceRole
from .sequence_number import SequenceNumber

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class BodyResource:
    """
    Details of a resource file needed to manufacture or package the main body of a
    product ● Added at revision 3.0.8.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sequence_number: Optional[SequenceNumber] = field(
        default=None,
        metadata={
            "name": "SequenceNumber",
            "type": "Element",
        },
    )
    resource_identifier: list[ResourceIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ResourceIdentifier",
            "type": "Element",
        },
    )
    resource_role: Optional[ResourceRole] = field(
        default=None,
        metadata={
            "name": "ResourceRole",
            "type": "Element",
        },
    )
    resource_file_detail: list[ResourceFileDetail] = field(
        default_factory=list,
        metadata={
            "name": "ResourceFileDetail",
            "type": "Element",
        },
    )
    resource_file_feature: list[ResourceFileFeature] = field(
        default_factory=list,
        metadata={
            "name": "ResourceFileFeature",
            "type": "Element",
        },
    )
    resource_file_description: list[ResourceFileDescription] = field(
        default_factory=list,
        metadata={
            "name": "ResourceFileDescription",
            "type": "Element",
        },
    )
    resource_file_content_description: list[ResourceFileContentDescription] = (
        field(
            default_factory=list,
            metadata={
                "name": "ResourceFileContentDescription",
                "type": "Element",
            },
        )
    )
    resource_file_link: list[ResourceFileLink] = field(
        default_factory=list,
        metadata={
            "name": "ResourceFileLink",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    resource_file_date: list[ResourceFileDate] = field(
        default_factory=list,
        metadata={
            "name": "ResourceFileDate",
            "type": "Element",
        },
    )
    refname: Optional[BodyResourceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[BodyResourceShortname] = field(
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
