from dataclasses import dataclass, field
from typing import Optional

from .body_manifest_refname import BodyManifestRefname
from .body_manifest_shortname import BodyManifestShortname
from .body_resource import BodyResource
from .list3 import List3
from .specification_bundle_name import SpecificationBundleName
from .specification_description import SpecificationDescription
from .specification_detail import SpecificationDetail
from .specification_feature import SpecificationFeature

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class BodyManifest:
    """
    Details of the resource files needed to manufacture or package the main body of
    a product ● Added at revision 3.0.8.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    specification_bundle_name: list[SpecificationBundleName] = field(
        default_factory=list,
        metadata={
            "name": "SpecificationBundleName",
            "type": "Element",
        },
    )
    specification_detail: list[SpecificationDetail] = field(
        default_factory=list,
        metadata={
            "name": "SpecificationDetail",
            "type": "Element",
        },
    )
    specification_feature: list[SpecificationFeature] = field(
        default_factory=list,
        metadata={
            "name": "SpecificationFeature",
            "type": "Element",
        },
    )
    specification_description: list[SpecificationDescription] = field(
        default_factory=list,
        metadata={
            "name": "SpecificationDescription",
            "type": "Element",
        },
    )
    body_resource: list[BodyResource] = field(
        default_factory=list,
        metadata={
            "name": "BodyResource",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[BodyManifestRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[BodyManifestShortname] = field(
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
