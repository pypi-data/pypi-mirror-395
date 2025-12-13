from dataclasses import dataclass, field
from typing import Optional

from .country_code import CountryCode
from .language_code import LanguageCode
from .language_refname import LanguageRefname
from .language_role import LanguageRole
from .language_shortname import LanguageShortname
from .list3 import List3
from .region_code import RegionCode
from .script_code import ScriptCode

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Language:
    """
    Details of a language and its relation to the product (eg language of text
    used, or original language from which the text was translated) ● Added
    &lt;RegionCode at revision 3.0.7.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    language_role: Optional[LanguageRole] = field(
        default=None,
        metadata={
            "name": "LanguageRole",
            "type": "Element",
            "required": True,
        },
    )
    language_code: Optional[LanguageCode] = field(
        default=None,
        metadata={
            "name": "LanguageCode",
            "type": "Element",
            "required": True,
        },
    )
    country_code: Optional[CountryCode] = field(
        default=None,
        metadata={
            "name": "CountryCode",
            "type": "Element",
        },
    )
    region_code: Optional[RegionCode] = field(
        default=None,
        metadata={
            "name": "RegionCode",
            "type": "Element",
        },
    )
    script_code: Optional[ScriptCode] = field(
        default=None,
        metadata={
            "name": "ScriptCode",
            "type": "Element",
        },
    )
    refname: Optional[LanguageRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[LanguageShortname] = field(
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
