from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List29(Enum):
    """
    Audience code type.

    Attributes:
        VALUE_01: ONIX audience codes Using a code from List 28
        VALUE_02: Proprietary audience scheme For example, a publisher’s
            or retailer’s own audience coding scheme. Note that a
            distinctive &lt;AudienceCodeTypeName&gt; is required with
            proprietary coding schemes
        VALUE_03: MPAA rating Motion Picture Association of America
            rating applied to movies
        VALUE_04: BBFC rating British Board of Film Classification
            rating applied to movies
        VALUE_05: FSK rating German FSK (Freiwillige Selbstkontrolle der
            Filmwirtschaft) rating applied to movies
        VALUE_06: BTLF audience code French Canadian audience code list,
            used by BTLF for Memento
        VALUE_07: Electre audience code Audience code used by Electre
            (France)
        VALUE_08: ANELE Tipo Spain: educational audience and material
            type code of the Asociación Nacional de Editores de Libros y
            Material de Enseñanza
        VALUE_09: AVI Code list used to specify reading levels for
            children’s books, used in Flanders, and formerly in the
            Netherlands – see also code 18
        VALUE_10: USK rating German USK (Unterhaltungssoftware
            Selbstkontrolle) rating applied to video or computer games
        VALUE_11: AWS Audience code used in Flanders
        VALUE_12: Schulform Type of school: codelist formerly maintained
            by VdS Bildungsmedien eV, the German association of
            educational media publishers at
            http://www.bildungsmedien.de/service/onixlisten/schulform_onix_codelist29_value12_0408.pdf.
            Deprecated – use Thema educational purpose qualifier (eg
            4Z-DE-BA – for German Elementary School) in &lt;Subject&gt;
            instead
        VALUE_13: Bundesland School region: codelist maintained by VdS
            Bildungsmedien eV, the German association of educational
            media publishers, indicating where products are licensed to
            be used in schools. See
            http://www.bildungsmedien.de/service/onixlisten/bundesland_onix_codelist29_value13_0408.pdf.
            Deprecated
        VALUE_14: Ausbildungsberuf Occupation: codelist for vocational
            training materials formerly maintained by VdS Bildungsmedien
            eV, the German association of educational media publishers
            at
            http://www.bildungsmedien.de/service/onixlisten/ausbildungsberufe_onix_codelist29_value14_0408.pdf.
            Deprecated – use Thema educational purpose qualifier (eg
            4Z-DE-UH – for specific German professional/vocational
            qualifications and degrees) in &lt;Subject&gt; instead
        VALUE_15: Suomalainen kouluasteluokitus Finnish school or
            college level
        VALUE_16: CBG age guidance UK Publishers Association, Children’s
            Book Group, coded indication of intended reader age, carried
            on book covers
        VALUE_17: BookData audience code Audience code used in NielsenIQ
            BookData services
        VALUE_18: AVI (revised) Code list used to specify reading levels
            for children’s books, used in the Netherlands – see also
            code 09
        VALUE_19: Lexile measure Lexile measure (the Lexile measure in
            &lt;AudienceCodeValue&gt; may optionally be prefixed by the
            Lexile code). Examples might be ‘880L’, ‘AD0L’ or ‘HL600L’.
            Deprecated – use &lt;Complexity&gt; instead
        VALUE_20: Fry Readability score Fry readability metric based on
            number of sentences and syllables per 100 words. Expressed
            as a number from 1 to 15 in &lt;AudienceCodeValue&gt;.
            Deprecated – use &lt;Complexity&gt; instead
        VALUE_21: Japanese Children’s audience code Children’s audience
            code (対象読者), two-digit encoding of intended target
            readership from 0–2 years up to High School level
        VALUE_22: ONIX Adult audience rating Publisher’s rating
            indicating suitability for a particular adult audience,
            using a code from List 203. Should only be used when the
            ONIX Audience code indicates a general adult audience (code
            01 from List 28)
        VALUE_23: Common European Framework of Reference for Language
            Learning (CEFR) Codes A1 to C2 indicating standardized level
            of language learning or teaching material, from beginner to
            advanced, defined by the Council of Europe (see
            http://www.coe.int/lang-CEFR)
        VALUE_24: Korean Publication Ethics Commission rating Rating
            used in Korea to control selling of books and e-books to
            minors. Current values are 0 (suitable for all) and 19 (only
            for sale to ages 19+). See http://www.kpec.or.kr/english/
        VALUE_25: IoE Book Band UK Institute of Education Book Bands for
            Guided Reading scheme (see
            http://www.ioe.ac.uk/research/4664.html).
            &lt;AudienceCodeValue&gt; is a color, eg ‘Pink A’ or
            ‘Copper’. Deprecated – use &lt;Complexity&gt; instead
        VALUE_26: FSK Lehr-/Infoprogramm Used for German videos/DVDs
            with educational or informative content; value for
            &lt;AudienceCodeValue&gt; must be either ‘Infoprogramm gemäß
            § 14 JuSchG’ or ‘Lehrprogramm gemäß § 14 JuSchG’
        VALUE_27: Intended audience language Where this is different
            from the language of the text of the book recorded in
            &lt;Language&gt;. &lt;AudienceCodeValue&gt; should be a
            value from List 74
        VALUE_28: PEGI rating Pan European Game Information rating used
            primarily for video games
        VALUE_29: Gymnasieprogram Code indicating the intended
            curriculum (eg Naturvetenskapsprogrammet, Estetica
            programmet) in Swedish higher secondary education
        VALUE_30: ISCED 2011 International Standard Classification of
            Education levels (2011), eg &lt;AudienceCodeValue&gt; 253 is
            ‘Lower secondary vocational education, level completion
            without direct access to upper secondary education’. Only
            for use in ONIX 3.0 or later. See
            http://uis.unesco.org/en/topic/international-standard-
            classification-education-isced
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
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
