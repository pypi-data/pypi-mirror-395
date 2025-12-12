from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List153(Enum):
    """
    Text type.

    Attributes:
        VALUE_01: Sender-defined text To be used only in circumstances
            where the parties to an exchange have agreed to include text
            which (a) is not for general distribution, and (b) cannot be
            coded elsewhere. If more than one type of text is sent, it
            must be identified by tagging within the text itself
        VALUE_02: Short description/annotation Of the product. Limited
            to a maximum of 350 characters. In ONIX 3.0, this is assumed
            to include markup characters. In ONIX 3.1 and later, this
            limit does not include markup
        VALUE_03: Description Of the product. Length unrestricted
        VALUE_04: Table of contents Used for a table of contents sent as
            a single text field, which may or may not carry structure
            expressed using XHTML
        VALUE_05: Primary cover copy Primary descriptive blurb usually
            taken from the back cover or jacket, or occasionally from
            the cover/jacket flaps. See also code 27
        VALUE_06: Review quote A quote taken from a review of the
            product or of the work in question where there is no need to
            take account of different editions
        VALUE_07: Review quote: previous edition A quote taken from a
            review of a previous edition of the work
        VALUE_08: Review quote: previous work A quote taken from a
            review of a previous work by the same author(s) or in the
            same series
        VALUE_09: Endorsement A quote usually provided by a celebrity or
            another author to promote a new book, not from a review
        VALUE_10: Promotional headline A promotional phrase which is
            intended to headline a description of the product
        VALUE_11: Feature Text describing a feature of a product to
            which the publisher wishes to draw attention for promotional
            purposes. Each separate feature should be described by a
            separate repeat, so that formatting can be applied at the
            discretion of the receiver of the ONIX record, or multiple
            features can be described using appropriate XHTML markup
        VALUE_12: Biographical note A note referring to all contributors
            to a product – NOT linked to a single contributor
        VALUE_13: Publisher’s notice A statement included by a publisher
            in fulfillment of contractual obligations, such as a
            disclaimer, sponsor statement, or legal notice of any sort.
            Note that the inclusion of such a notice cannot and does not
            imply that a user of the ONIX record is obliged to reproduce
            it
        VALUE_14: Excerpt A short excerpt from the main text of the work
        VALUE_15: Index Used for an index sent as a single text field,
            which may be structured using XHTML
        VALUE_16: Short description/annotation for collection (of which
            the product is a part.) Limited to a maximum of 350
            characters
        VALUE_17: Description for collection (of which the product is a
            part.) Length unrestricted
        VALUE_18: New feature As code 11 but used for a new feature of
            this edition or version
        VALUE_19: Version history
        VALUE_20: Open access statement Short summary statement of open
            access status and any related conditions (eg ‘Open access –
            no commercial use’), primarily for marketing purposes.
            Should always be accompanied by a link to the complete
            license (see &lt;EpubLicense&gt; or code 99 in List 158)
        VALUE_21: Digital exclusivity statement Short summary statement
            that the product is available only in digital formats (eg
            ‘Digital exclusive’). If a non-digital version is planned,
            &lt;ContentDate&gt; should be used to specify the date when
            exclusivity will end (use content date role code 15). If a
            non-digital version is available, the statement should not
            be included
        VALUE_22: Official recommendation For example a recommendation
            or approval provided by a ministry of education or other
            official body. Use &lt;Text&gt; to provide details and
            ideally use &lt;TextSourceCorporate&gt; to name the approver
        VALUE_23: JBPA description Short description in format specified
            by Japanese Book Publishers Association
        VALUE_24: schema.org snippet JSON-LD snippet suitable for use
            within an HTML &lt;script type="application/ld+json"&gt;
            tag, containing structured metadata suitable for use with
            schema.org
        VALUE_25: Errata
        VALUE_26: Introduction Introduction, preface or the text of
            other preliminary material, sent as a single text field,
            which may be structured using XHTML
        VALUE_27: Secondary cover copy Secondary descriptive blurb taken
            from the cover/jacket flaps, or occasionally from the back
            cover or jacket, used only when there are two separate texts
            and the primary text is included using code 05
        VALUE_28: Full cast and credit list For use with dramatized
            audiobooks, filmed entertainment etc, for a cast list sent
            as a single text field, which may or may not carry structure
            expressed using XHTML
        VALUE_29: Bibliography Complete list of books by the author(s),
            supplied as a single text field, which may be structured
            using (X)HTML
        VALUE_30: Abstract Formal summary of content (normally used with
            academic and scholarly content only)
        VALUE_31: Rules or instructions Eg for a game or kit – as
            supplied with the product
        VALUE_32: List of contents Eg for a game, kit. Note: use code 04
            for a Table of Contents of a book
        VALUE_33: Short description/annotation for imprint Length
            limited to a maximum of 350 characters
        VALUE_34: Description for imprint Length unrestricted
        VALUE_35: Short description/annotation for publisher Length
            limited to a maximum of 350 characters
        VALUE_36: Description for publisher Length unrestricted
        VALUE_37: Cover line (US) Reading line – line of usually
            explanatory copy on cover, somewhat like a subtitle but not
            on the title page and added by the publisher, eg ‘with 125
            illustrated recipes’
        VALUE_38: Special cover statement Short summary description of
            special nature of cover or jacket, for use with special
            editions (use with Edition type SPE), or with variant
            covers, when there is also a ‘standard’ cover
        VALUE_39: List of bonus contents Short summary description of
            bonus content (when there is also a ‘standard’ set of
            contents). Bonus material may include a new or extra
            foreword, additional illustrations, previously-unpublished
            bonus chapters (for these use with Edition type ENL), or for
            teaser chapters, author interview etc (do not use ENL)
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
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_34 = "34"
    VALUE_35 = "35"
    VALUE_36 = "36"
    VALUE_37 = "37"
    VALUE_38 = "38"
    VALUE_39 = "39"
