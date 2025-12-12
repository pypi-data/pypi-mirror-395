from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List28(Enum):
    """
    Audience type.

    Attributes:
        VALUE_01: General / adult For a non-specialist or ‘popular’
            adult audience. Consider also adding an ONIX Adult audience
            rating
        VALUE_02: Children For a young audience typically up to about
            the age of 12, not specifically for any educational purpose.
            An audience range should also be included
        VALUE_03: Teenage For a teenage or ‘young adult’ audience
            typically from about the age of 12 to the late teens, not
            specifically for any educational purpose. An audience range
            should also be included
        VALUE_04: Primary and secondary education Kindergarten, pre-
            school, primary / elementary or secondary / high school
            education. Note ‘secondary’ includes both level 2 and level
            3 secondary education as defined in UNESCO’s ISCED 2011 (see
            http://uis.unesco.org/en/topic/international-standard-
            classification-education-isced). An audience range should
            also be included
        VALUE_11: Pre-primary education Equivalent to UNESCO’s ISCED
            Level 0 – see http://uis.unesco.org/en/topic/international-
            standard-classification-education-isced (note codes 11–14
            are specific subsets of the Primary and secondary education
            audience, code 04). Only for use in ONIX 3.0 or later
        VALUE_12: Primary education Equivalent to ISCED Level 1. Only
            for use in ONIX 3.0 or later
        VALUE_13: Lower secondary education Equivalent to ISCED Level 2
            (general and vocational). Only for use in ONIX 3.0 or later
        VALUE_14: Upper secondary education Equivalent to ISCED Level 3
            (general and vocational). Only for use in ONIX 3.0 or later
        VALUE_05: Tertiary education For tertiary education typically in
            universities and colleges of higher education, equivalent to
            ISCED Levels 5–7
        VALUE_06: Professional and scholarly For an expert adult
            audience, including professional development and academic
            research
        VALUE_08: Adult education For any adult audience in a formal or
            semi-formal learning setting, eg vocational training and
            apprenticeships (collectively, equivalent to ISCED Level 4),
            or practical or recreational learning for adults
        VALUE_07: EFL / TEFL / TESOL Intended for use in teaching and
            learning English as a second, non-native or additional
            language. Indication of the language level (eg CEFR) should
            be included where possible. An audience range should also be
            included if the product is (also) suitable for use in
            primary and secondary education
        VALUE_09: Second / additional language teaching Intended for use
            in teaching and learning second, non-native or additional
            languages (other than English), for example teaching German
            to Spanish speakers. Indication of the language level (eg
            CEFR) should be included where possible. An audience range
            should also be included if the product is (also) suitable
            for use in primary and secondary education. Prefer code 07
            for products specific to teaching English
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_08 = "08"
    VALUE_07 = "07"
    VALUE_09 = "09"
