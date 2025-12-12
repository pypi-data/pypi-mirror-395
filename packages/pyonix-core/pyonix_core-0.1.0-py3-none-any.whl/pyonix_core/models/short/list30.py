from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List30(Enum):
    """
    Audience range qualifier.

    Attributes:
        VALUE_11: US school grade range Values for
            &lt;AudienceRangeValue&gt; are specified in List 77
        VALUE_12: UK school grade Values are to be defined by BIC for
            England and Wales, Scotland and N Ireland
        VALUE_15: Reading speed, words per minute Values in
            &lt;AudienceRangeValue&gt; must be integers
        VALUE_16: Interest age, months For use up to 36 months only, or
            up to 42 months in Audience range value (2) only: values in
            &lt;AudienceRangeValue&gt; must be integers. Should not be
            used when an Audience range with qualifier code 17 is
            present
        VALUE_17: Interest age, years Values in
            &lt;AudienceRangeValue&gt; must be integers
        VALUE_18: Reading age, years Values in
            &lt;AudienceRangeValue&gt; must be integers
        VALUE_19: Spanish school grade Spain: combined grade and region
            code, maintained by the Ministerio de Educación
        VALUE_20: Skoletrinn Norwegian educational level for primary and
            secondary education
        VALUE_21: Nivå Swedish educational qualifier (code)
        VALUE_22: Italian school grade
        VALUE_23: Schulform Deprecated – assigned in error: see List 29
        VALUE_24: Bundesland Deprecated – assigned in error: see List 29
        VALUE_25: Ausbildungsberuf Deprecated – assigned in error: see
            List 29
        VALUE_26: Canadian school grade range Values for
            &lt;AudienceRangeValue&gt; are specified in List 77
        VALUE_27: Finnish school grade range
        VALUE_28: Finnish Upper secondary school course Lukion kurssi
        VALUE_29: Chinese School Grade range Values are P, K, 1–17
            (including college-level audiences), see List 227
        VALUE_30: French school cycles / classes Detailed French
            educational level classification. Values are defined by
            ScoLOMFR, see
            http://data.education.fr/voc/scolomfr/scolomfr-voc-022 –
            Cycles de l’enseignement scolaire. See also code 34
        VALUE_31: Brazil Education level Nível de Educação do Brasil,
            see List 238. Only for use in ONIX 3.0 or later
        VALUE_32: French educational levels Basic French educational
            level classification. Values are defined by ScoLOMFR. Only
            for use in ONIX 3.0 or later. See
            http://data.education.fr/voc/scolomfr/scolomfr-voc-012
        VALUE_33: Finnish Upper secondary school course (2021+) Only for
            use in ONIX 3.0 or later
        VALUE_34: Detailed French educational levels Detailed French
            educational level classification. Values are defined by
            ScoLOMFR. Only for use in ONIX 3.0 or later. See
            http://data.education.fr/voc/scolomfr/scolomfr-voc-022 –
            Niveau éducatif détaillé. See also code 30
    """

    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_34 = "34"
