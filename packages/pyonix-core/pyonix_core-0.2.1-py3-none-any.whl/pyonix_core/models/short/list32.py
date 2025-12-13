from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List32(Enum):
    """
    Complexity scheme identifier.

    Attributes:
        VALUE_01: Lexile code For example AD or HL. Deprecated in ONIX 3
            – use code 06 instead
        VALUE_02: Lexile number For example 880L. Deprecated in ONIX 3 –
            use code 06 instead
        VALUE_03: Fry Readability score Fry readability metric based on
            number of sentences and syllables per 100 words. Expressed
            as an integer from 1 to 15 in &lt;ComplexityCode&gt;
        VALUE_04: IoE Book Band UK Institute of Education Book Bands for
            Guided Reading scheme (see https://www.ucl.ac.uk/reading-
            recovery-europe/ilc/publications/which-book-why).
            &lt;ComplexityCode&gt; is a color, eg ‘Pink A’ or ‘Copper’
        VALUE_05: Fountas &amp; Pinnell Text Level Gradient
            &lt;ComplexityCode&gt; is a code from ‘A’ to Z+’. See
            http://www.fountasandpinnellleveledbooks.com/aboutLeveledTexts.aspx
        VALUE_06: Lexile measure The Lexile measure in
            &lt;ComplexityCode&gt; combines MetaMetrics’ Lexile number
            (for example 620L or 880L) and optionally the Lexile code
            (for example AD or HL). Examples might be ‘880L’, ‘AD0L’ or
            ‘HL600L’. Applies to English text. See
            https://lexile.com/about-lexile/lexile-overview/
        VALUE_07: ATOS for Books Advantage-TASA Open Standard book
            readability score, used for example within the Renaissance
            Learning Accelerated Reader scheme. &lt;ComplexityCode&gt;
            is the ‘Book Level’, a real number between 0 and 17. See
            http://www.renaissance.com/products/accelerated-reader/atos-
            analyzer
        VALUE_08: Flesch-Kincaid Grade Level Flesch-Kincaid Grade Level
            Formula, a standard readability measure based on the
            weighted number of syllables per word and words per
            sentence. &lt;ComplexityCode&gt; is a real number typically
            between about -1 and 20
        VALUE_09: Guided Reading Level Use this code for books levelled
            by the publisher or a third party using the Fountas and
            Pinnell Guided Reading methodology
        VALUE_10: Reading Recovery Level Used for books aimed at K-2
            literacy intervention. &lt;ComplexityCode&gt; is an integer
            between 1 and 20
        VALUE_11: LIX Swedish ‘läsbarhetsindex’ readability index used
            in Scandinavia. Only for use in ONIX 3.0 or later
        VALUE_12: Lexile Audio measure Lexile Audio measure from
            MetaMetrics’ Framework for Listening. The code in
            &lt;ComplexityCode&gt; indicates the difficulty of
            comprehension of audio material (for example 600L or 1030L).
            Only for use in ONIX 3.0 or later. See
            https://lexile.global/the-lexile-framework-for-listening/
        VALUE_13: Lexile measure (Spanish) Metametrics’ Lexile measure
            for Spanish text. See
            https://lexile.com/educators/understanding-lexile-
            measures/lexile-measures-spanish/ Only for use in ONIX 3.0
            or later
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
