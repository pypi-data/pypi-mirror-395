from dataclasses import dataclass, field
from typing import Optional

from .addressee import Addressee
from .default_currency_code import DefaultCurrencyCode
from .default_language_of_text import DefaultLanguageOfText
from .default_price_type import DefaultPriceType
from .header_refname import HeaderRefname
from .header_shortname import HeaderShortname
from .list3 import List3
from .message_note import MessageNote
from .message_number import MessageNumber
from .message_repeat import MessageRepeat
from .sender import Sender
from .sent_date_time import SentDateTime

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Header:
    """
    Container for message metadata ● Modified cardinality of &lt;MessageNote&gt; at
    revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sender: Optional[Sender] = field(
        default=None,
        metadata={
            "name": "Sender",
            "type": "Element",
            "required": True,
        },
    )
    addressee: list[Addressee] = field(
        default_factory=list,
        metadata={
            "name": "Addressee",
            "type": "Element",
        },
    )
    message_number: Optional[MessageNumber] = field(
        default=None,
        metadata={
            "name": "MessageNumber",
            "type": "Element",
        },
    )
    message_repeat: Optional[MessageRepeat] = field(
        default=None,
        metadata={
            "name": "MessageRepeat",
            "type": "Element",
        },
    )
    sent_date_time: Optional[SentDateTime] = field(
        default=None,
        metadata={
            "name": "SentDateTime",
            "type": "Element",
            "required": True,
        },
    )
    message_note: list[MessageNote] = field(
        default_factory=list,
        metadata={
            "name": "MessageNote",
            "type": "Element",
        },
    )
    default_language_of_text: Optional[DefaultLanguageOfText] = field(
        default=None,
        metadata={
            "name": "DefaultLanguageOfText",
            "type": "Element",
        },
    )
    default_price_type: Optional[DefaultPriceType] = field(
        default=None,
        metadata={
            "name": "DefaultPriceType",
            "type": "Element",
        },
    )
    default_currency_code: Optional[DefaultCurrencyCode] = field(
        default=None,
        metadata={
            "name": "DefaultCurrencyCode",
            "type": "Element",
        },
    )
    refname: Optional[HeaderRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[HeaderShortname] = field(
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
