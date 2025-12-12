from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .specification_bundle_name_refname import SpecificationBundleNameRefname
from .specification_bundle_name_shortname import (
    SpecificationBundleNameShortname,
)
from .specification_bundle_name_type_name import (
    SpecificationBundleNameTypeName,
)
from .specification_bundle_name_value import SpecificationBundleNameValue

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class SpecificationBundleName:
    """
    ● Added at revision 3.0.8.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    specification_bundle_name_type_name: Optional[
        SpecificationBundleNameTypeName
    ] = field(
        default=None,
        metadata={
            "name": "SpecificationBundleNameTypeName",
            "type": "Element",
            "required": True,
        },
    )
    specification_bundle_name_value: Optional[SpecificationBundleNameValue] = (
        field(
            default=None,
            metadata={
                "name": "SpecificationBundleNameValue",
                "type": "Element",
                "required": True,
            },
        )
    )
    refname: Optional[SpecificationBundleNameRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SpecificationBundleNameShortname] = field(
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
