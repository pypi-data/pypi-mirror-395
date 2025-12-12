from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List144(Enum):
    """
    E-publication technical protection.

    Attributes:
        VALUE_00: None Has no technical protection
        VALUE_01: DRM Has DRM protection
        VALUE_02: Digital watermarking Has digital watermarking
        VALUE_03: Adobe DRM Has DRM protection applied by the Adobe CS4
            Content Server Package or by the Adobe ADEPT hosted service
        VALUE_04: Apple DRM Has FairPlay DRM protection applied via
            Apple proprietary online store
        VALUE_05: OMA DRM Has OMA v2 DRM protection applied, as used to
            protect some mobile phone content
        VALUE_06: Readium LCP DRM Has Licensed Content Protection DRM
            applied by a Readium License Server. See
            https://readium.org/lcp-specs/
        VALUE_07: Sony DRM Has Sony DADC User Rights Management (URMS)
            DRM protection applied
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
