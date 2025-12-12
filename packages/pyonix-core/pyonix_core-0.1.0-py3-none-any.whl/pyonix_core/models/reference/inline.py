from dataclasses import dataclass, field
from typing import ForwardRef, Optional

from .a_dir import ADir
from .abbr_dir import AbbrDir
from .acronym_dir import AcronymDir
from .address_dir import AddressDir
from .area import Area
from .b_dir import BDir
from .bdo_dir import BdoDir
from .big_dir import BigDir
from .blockquote_dir import BlockquoteDir
from .br import Br
from .caption_dir import CaptionDir
from .cite_dir import CiteDir
from .code_dir import CodeDir
from .col import Col
from .colgroup import Colgroup
from .dd_dir import DdDir
from .dfn_dir import DfnDir
from .div_dir import DivDir
from .dl_dir import DlDir
from .dt_dir import DtDir
from .em_dir import EmDir
from .h1_dir import H1Dir
from .h2_dir import H2Dir
from .h3_dir import H3Dir
from .h4_dir import H4Dir
from .h5_dir import H5Dir
from .h6_dir import H6Dir
from .hr import Hr
from .i_dir import IDir
from .img import Img
from .kbd_dir import KbdDir
from .li_dir import LiDir
from .map_dir import MapDir
from .ol_dir import OlDir
from .p_dir import PDir
from .pre_dir import PreDir
from .q_dir import QDir
from .rb_dir import RbDir
from .rbc_dir import RbcDir
from .rp import Rp
from .rt_dir import RtDir
from .rtc_dir import RtcDir
from .ruby_dir import RubyDir
from .samp_dir import SampDir
from .scope import Scope
from .shape import Shape
from .small_dir import SmallDir
from .span_dir import SpanDir
from .strong_dir import StrongDir
from .sub_dir import SubDir
from .sup_dir import SupDir
from .table_dir import TableDir
from .tbody_align import TbodyAlign
from .tbody_dir import TbodyDir
from .tbody_valign import TbodyValign
from .td_align import TdAlign
from .td_dir import TdDir
from .td_valign import TdValign
from .tfoot_align import TfootAlign
from .tfoot_dir import TfootDir
from .tfoot_valign import TfootValign
from .tframe import Tframe
from .th_align import ThAlign
from .th_dir import ThDir
from .th_valign import ThValign
from .thead_align import TheadAlign
from .thead_dir import TheadDir
from .thead_valign import TheadValign
from .tr_align import TrAlign
from .tr_dir import TrDir
from .tr_valign import TrValign
from .trules import Trules
from .tt_dir import TtDir
from .ul_dir import UlDir
from .var_dir import VarDir

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Inline:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "a",
                    "type": ForwardRef("A"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "q",
                    "type": ForwardRef("Q"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "acronym",
                    "type": ForwardRef("Acronym"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "abbr",
                    "type": ForwardRef("Abbr"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "cite",
                    "type": ForwardRef("Cite"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "var",
                    "type": ForwardRef("Var"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "kbd",
                    "type": ForwardRef("Kbd"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "samp",
                    "type": ForwardRef("Samp"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "code",
                    "type": ForwardRef("Code"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "dfn",
                    "type": ForwardRef("Dfn"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "strong",
                    "type": ForwardRef("Strong"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "em",
                    "type": ForwardRef("Em"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "small",
                    "type": ForwardRef("Small"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "big",
                    "type": ForwardRef("Big"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "b",
                    "type": ForwardRef("B"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "i",
                    "type": ForwardRef("I"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "tt",
                    "type": ForwardRef("Tt"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "map",
                    "type": ForwardRef("Map"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "bdo",
                    "type": ForwardRef("Bdo"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "span",
                    "type": ForwardRef("Span"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
            ),
        },
    )


@dataclass
class Abbr(Inline):
    class Meta:
        name = "abbr"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[AbbrDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Acronym(Inline):
    class Meta:
        name = "acronym"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[AcronymDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Address(Inline):
    class Meta:
        name = "address"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[AddressDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class B(Inline):
    class Meta:
        name = "b"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[BDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Bdo(Inline):
    class Meta:
        name = "bdo"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[BdoDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Big(Inline):
    class Meta:
        name = "big"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[BigDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Caption(Inline):
    class Meta:
        name = "caption"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[CaptionDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Cite(Inline):
    class Meta:
        name = "cite"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[CiteDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Code(Inline):
    class Meta:
        name = "code"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[CodeDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Dfn(Inline):
    class Meta:
        name = "dfn"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[DfnDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Dt(Inline):
    class Meta:
        name = "dt"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[DtDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Em(Inline):
    class Meta:
        name = "em"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[EmDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class H1(Inline):
    class Meta:
        name = "h1"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[H1Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class H2(Inline):
    class Meta:
        name = "h2"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[H2Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class H3(Inline):
    class Meta:
        name = "h3"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[H3Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class H4(Inline):
    class Meta:
        name = "h4"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[H4Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class H5(Inline):
    class Meta:
        name = "h5"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[H5Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class H6(Inline):
    class Meta:
        name = "h6"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[H6Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class I(Inline):
    class Meta:
        name = "i"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[IDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Kbd(Inline):
    class Meta:
        name = "kbd"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[KbdDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class P(Inline):
    class Meta:
        name = "p"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[PDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Q(Inline):
    class Meta:
        name = "q"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[QDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cite: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Samp(Inline):
    class Meta:
        name = "samp"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[SampDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Small(Inline):
    class Meta:
        name = "small"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[SmallDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Span(Inline):
    class Meta:
        name = "span"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[SpanDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Strong(Inline):
    class Meta:
        name = "strong"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[StrongDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Sub(Inline):
    class Meta:
        name = "sub"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[SubDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Sup(Inline):
    class Meta:
        name = "sup"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[SupDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Tt(Inline):
    class Meta:
        name = "tt"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[TtDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Var(Inline):
    class Meta:
        name = "var"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[VarDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Block:
    table: list["Table"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    div: list["Div"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    blockquote: list["Blockquote"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    pre: list["Pre"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    hr: list[Hr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    dl: list["Dl"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    ol: list["Ol"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    ul: list["Ul"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    h6: list[H6] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    h5: list[H5] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    h4: list[H4] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    h3: list[H3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    h2: list[H2] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )
    h1: list[H1] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.0/reference",
        },
    )


@dataclass
class AContent:
    class Meta:
        name = "a.content"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "map",
                    "type": ForwardRef("Map"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "bdo",
                    "type": Bdo,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "span",
                    "type": Span,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "small",
                    "type": Small,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "big",
                    "type": Big,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "b",
                    "type": B,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "i",
                    "type": I,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "tt",
                    "type": Tt,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sup",
                    "type": Sup,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sub",
                    "type": Sub,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "q",
                    "type": Q,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "acronym",
                    "type": Acronym,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "abbr",
                    "type": Abbr,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "cite",
                    "type": Cite,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "var",
                    "type": Var,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "kbd",
                    "type": Kbd,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "samp",
                    "type": Samp,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "code",
                    "type": Code,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "dfn",
                    "type": Dfn,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "strong",
                    "type": Strong,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "em",
                    "type": Em,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
            ),
        },
    )


@dataclass
class A(AContent):
    class Meta:
        name = "a"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[ADir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charset: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rev: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    accesskey: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shape: Shape = field(
        default=Shape.RECT,
        metadata={
            "type": "Attribute",
        },
    )
    coords: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    tabindex: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    onfocus: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    onblur: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Blockquote(Block):
    class Meta:
        name = "blockquote"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[BlockquoteDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cite: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Flow:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "table",
                    "type": ForwardRef("Table"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "p",
                    "type": P,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "div",
                    "type": ForwardRef("Div"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "blockquote",
                    "type": Blockquote,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "pre",
                    "type": ForwardRef("Pre"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "hr",
                    "type": Hr,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "address",
                    "type": Address,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "dl",
                    "type": ForwardRef("Dl"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "ol",
                    "type": ForwardRef("Ol"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "ul",
                    "type": ForwardRef("Ul"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "h6",
                    "type": H6,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "h5",
                    "type": H5,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "h4",
                    "type": H4,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "h3",
                    "type": H3,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "h2",
                    "type": H2,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "h1",
                    "type": H1,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "a",
                    "type": ForwardRef("A"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sup",
                    "type": Sup,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sub",
                    "type": Sub,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "q",
                    "type": Q,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "acronym",
                    "type": Acronym,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "abbr",
                    "type": Abbr,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "cite",
                    "type": Cite,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "var",
                    "type": Var,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "kbd",
                    "type": Kbd,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "samp",
                    "type": Samp,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "code",
                    "type": Code,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "dfn",
                    "type": Dfn,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "strong",
                    "type": Strong,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "em",
                    "type": Em,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "small",
                    "type": Small,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "big",
                    "type": Big,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "b",
                    "type": B,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "i",
                    "type": I,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "tt",
                    "type": Tt,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "map",
                    "type": ForwardRef("Map"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "bdo",
                    "type": Bdo,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "span",
                    "type": Span,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
            ),
        },
    )


@dataclass
class PreContent:
    class Meta:
        name = "pre.content"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "a",
                    "type": A,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "span",
                    "type": Span,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "bdo",
                    "type": Bdo,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "map",
                    "type": ForwardRef("Map"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "tt",
                    "type": Tt,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "i",
                    "type": I,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "b",
                    "type": B,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sup",
                    "type": Sup,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sub",
                    "type": Sub,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "q",
                    "type": Q,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "acronym",
                    "type": Acronym,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "abbr",
                    "type": Abbr,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "cite",
                    "type": Cite,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "var",
                    "type": Var,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "kbd",
                    "type": Kbd,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "samp",
                    "type": Samp,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "code",
                    "type": Code,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "dfn",
                    "type": Dfn,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "strong",
                    "type": Strong,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "em",
                    "type": Em,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
            ),
        },
    )


@dataclass
class Dd(Flow):
    class Meta:
        name = "dd"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[DdDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Div(Flow):
    class Meta:
        name = "div"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[DivDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Li(Flow):
    class Meta:
        name = "li"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[LiDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Pre(PreContent):
    class Meta:
        name = "pre"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[PreDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Td(Flow):
    class Meta:
        name = "td"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[TdDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    abbr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    axis: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    headers: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    scope: Optional[Scope] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rowspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    colspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[TdAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TdValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Th(Flow):
    class Meta:
        name = "th"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[ThDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    abbr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    axis: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    headers: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    scope: Optional[Scope] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rowspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    colspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[ThAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[ThValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Dl:
    class Meta:
        name = "dl"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    dt: list[Dt] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    dd: list[Dd] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[DlDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Ol:
    class Meta:
        name = "ol"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    li: list[Li] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[OlDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Tr:
    class Meta:
        name = "tr"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    th: list[Th] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    td: list[Td] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[TrDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[TrAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TrValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Ul:
    class Meta:
        name = "ul"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    li: list[Li] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[UlDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Tbody:
    class Meta:
        name = "tbody"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[TbodyDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[TbodyAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TbodyValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Tfoot:
    class Meta:
        name = "tfoot"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[TfootDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[TfootAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TfootValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Thead:
    class Meta:
        name = "thead"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[TheadDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[TheadAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TheadValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Table:
    class Meta:
        name = "table"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    caption: Optional[Caption] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    col: list[Col] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    colgroup: list[Colgroup] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    thead: Optional[Thead] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    tfoot: Optional[Tfoot] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    tbody: list[Tbody] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[TableDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    summary: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    border: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    frame: Optional[Tframe] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rules: Optional[Trules] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cellspacing: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cellpadding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Map:
    class Meta:
        name = "map"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    div: list[Div] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    blockquote: list[Blockquote] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    pre: list[Pre] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    hr: list[Hr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    dl: list[Dl] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    h6: list[H6] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    h5: list[H5] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    h4: list[H4] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    h3: list[H3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    h2: list[H2] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    h1: list[H1] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    area: list[Area] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[MapDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class RubyContent:
    class Meta:
        name = "ruby.content"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "a",
                    "type": A,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "map",
                    "type": Map,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "bdo",
                    "type": Bdo,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "span",
                    "type": Span,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "small",
                    "type": Small,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "big",
                    "type": Big,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "b",
                    "type": B,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "i",
                    "type": I,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "tt",
                    "type": Tt,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sup",
                    "type": Sup,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "sub",
                    "type": Sub,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "q",
                    "type": Q,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "acronym",
                    "type": Acronym,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "abbr",
                    "type": Abbr,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "cite",
                    "type": Cite,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "var",
                    "type": Var,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "kbd",
                    "type": Kbd,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "samp",
                    "type": Samp,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "code",
                    "type": Code,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "dfn",
                    "type": Dfn,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "strong",
                    "type": Strong,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
                {
                    "name": "em",
                    "type": Em,
                    "namespace": "http://ns.editeur.org/onix/3.0/reference",
                },
            ),
        },
    )


@dataclass
class Rb(RubyContent):
    class Meta:
        name = "rb"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[RbDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Rt(RubyContent):
    class Meta:
        name = "rt"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[RtDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rbspan: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Rbc:
    class Meta:
        name = "rbc"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    rb: list[Rb] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[RbcDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Rtc:
    class Meta:
        name = "rtc"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    rt: list[Rt] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[RtcDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Ruby:
    class Meta:
        name = "ruby"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    rb: Optional[Rb] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    rt: list[Rt] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 2,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    rp: list[Rp] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 2,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    rbc: Optional[Rbc] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    rtc: list[Rtc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 2,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[RubyDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
