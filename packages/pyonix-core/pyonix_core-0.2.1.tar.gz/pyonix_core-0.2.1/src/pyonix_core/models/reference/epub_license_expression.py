from dataclasses import dataclass, field
from typing import Optional

from .epub_license_expression_link import EpubLicenseExpressionLink
from .epub_license_expression_refname import EpubLicenseExpressionRefname
from .epub_license_expression_shortname import EpubLicenseExpressionShortname
from .epub_license_expression_type import EpubLicenseExpressionType
from .epub_license_expression_type_name import EpubLicenseExpressionTypeName
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class EpubLicenseExpression:
    """
    Details of a particular expression of an end user license ● Added at revision
    3.0.2.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    epub_license_expression_type: Optional[EpubLicenseExpressionType] = field(
        default=None,
        metadata={
            "name": "EpubLicenseExpressionType",
            "type": "Element",
            "required": True,
        },
    )
    epub_license_expression_type_name: Optional[
        EpubLicenseExpressionTypeName
    ] = field(
        default=None,
        metadata={
            "name": "EpubLicenseExpressionTypeName",
            "type": "Element",
        },
    )
    epub_license_expression_link: Optional[EpubLicenseExpressionLink] = field(
        default=None,
        metadata={
            "name": "EpubLicenseExpressionLink",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[EpubLicenseExpressionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[EpubLicenseExpressionShortname] = field(
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
