from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List158(Enum):
    """
    Resource content type.

    Attributes:
        VALUE_01: Front cover 2D
        VALUE_02: Back cover 2D
        VALUE_56: Spine image 2D, portrait orientation
        VALUE_57: Spine panorama image 2D, image spans multiple upright
            spines
        VALUE_03: Cover / pack Not limited to front or back, including
            3D perspective
        VALUE_04: Contributor picture Photograph or portrait of
            contributor(s)
        VALUE_05: Collection image / artwork
        VALUE_06: Collection logo
        VALUE_07: Product image / artwork For example, an isolated image
            from the front cover (without text), image of a completed
            jigsaw
        VALUE_08: Product logo
        VALUE_09: Publisher logo
        VALUE_10: Imprint logo
        VALUE_11: Contributor interview
        VALUE_12: Contributor presentation Contributor presentation
            and/or commentary
        VALUE_13: Contributor reading
        VALUE_14: Contributor event schedule Link to a schedule in
            iCalendar format
        VALUE_15: Sample content For example: a short excerpt, sample
            text or a complete sample chapter, page images, screenshots
            etc
        VALUE_16: Widget A ‘look inside’ feature presented as a small
            embeddable application
        VALUE_17: Review Review text held in a separate downloadable
            file, not in the ONIX record. Equivalent of code 06 in List
            153. Use the &lt;TextContent&gt; composite for review quotes
            carried in the ONIX record. Use the &lt;CitedContent&gt;
            composite for a third-party review which is referenced from
            the ONIX record. Use &lt;SupportingResource&gt; for review
            text offered as a separate file resource for reproduction as
            part of promotional material for the product
        VALUE_18: Commentary / discussion For example a publisher’s
            podcast episode, social media message, newsletter issue,
            other commentary
        VALUE_19: Reading group guide
        VALUE_20: Teacher’s guide Including associated teacher /
            instructor resources
        VALUE_21: Feature article Feature article provided by publisher
        VALUE_22: Character ‘interview’ Fictional character ‘interview’
        VALUE_23: Wallpaper / screensaver
        VALUE_24: Press release
        VALUE_25: Table of contents A table of contents held in a
            separate downloadable file, not in the ONIX record.
            Equivalent of code 04 in List 153. Use the
            &lt;TextContent&gt; composite for a table of contents
            carried in the ONIX record. Use &lt;SupportingResource&gt;
            for text offered as a separate file resource
        VALUE_26: Trailer A promotional video (or audio), similar to a
            movie trailer (sometimes referred to as a ‘book trailer’)
        VALUE_27: Cover thumbnail Intended ONLY for transitional use,
            where ONIX 2.1 records referencing existing thumbnail assets
            of unknown pixel size are being re-expressed in ONIX 3.0.
            Use code 01 for all new cover assets, and where the pixel
            size of older assets is known
        VALUE_28: Full content The full content of the product (or the
            product itself), supplied for example to support full-text
            search or indexing
        VALUE_29: Full cover Includes cover, back cover, spine and –
            where appropriate – any flaps
        VALUE_30: Master brand logo
        VALUE_31: Description Descriptive text in a separate
            downloadable file, not in the ONIX record. Equivalent of
            code 03 in List 153. Use the &lt;TextContent&gt; composite
            for descriptions carried in the ONIX record. Use
            &lt;SupportingResource&gt; for text offered as a separate
            file resource for reproduction as part of promotional
            material for the product
        VALUE_32: Index Index text held in a separate downloadable file,
            not in the ONIX record. Equivalent of code 15 in List 153.
            Use the &lt;TextContent&gt; composite for index text carried
            in the ONIX record. Use &lt;SupportingResource&gt; for an
            index offered as a separate file resource
        VALUE_33: Student’s guide Including associated student / learner
            resources
        VALUE_34: Publisher’s catalogue For example a PDF or other
            digital representation of a publisher’s ‘new titles’ or
            range catalog
        VALUE_35: Online advertisement panel For example a banner ad for
            the product. Pixel dimensions should typically be included
            in &lt;ResourceVersionFeature&gt;
        VALUE_36: Online advertisement page (de: ‘Búhnenbild’)
        VALUE_37: Promotional event material For example, posters,
            logos, banners, advertising templates for use in connection
            with a promotional event
        VALUE_38: Digital review copy Availability of a digital review,
            evaluation or sample copy, or a digital proof copy, which
            may be limited to authorized users or account holders, but
            should otherwise be fully readable and functional
        VALUE_39: Instructional material For example, a video, PDF, web
            page or app showing how to assemble, use or maintain the
            product, that is separate from the product itself
        VALUE_40: Errata
        VALUE_41: Introduction Introduction, preface or other
            preliminary material in a separate resource file
        VALUE_42: Collection description Descriptive material in a
            separate resource file, not in the ONIX record. Equivalent
            of code 17 in List 153. Use the &lt;TextContent&gt;
            composite for collection descriptions carried in the ONIX
            record. Use &lt;SupportingResource&gt; for material (which
            need not be solely only) offered as a separate file resource
            for reproduction as part of promotional material for the
            product and collection
        VALUE_43: Bibliography Complete list of books by the author(s),
            supplied as a separate resource file
        VALUE_44: Abstract Formal summary of content (normally used with
            academic and scholarly content only)
        VALUE_45: Cover holding image Image that may be used for
            promotional purposes in place of a front cover, ONLY where
            the front cover itself cannot be provided or used for any
            reason. Typically, holding images may comprise logos,
            artwork or an unfinished front cover image. Senders should
            ensure removal of the holding image from the record as soon
            as a cover image is available. Recipients must ensure
            replacement of the holding image with the cover image when
            it is supplied
        VALUE_46: Rules or instructions Eg for a game or kit – as
            supplied with the product
        VALUE_47: Transcript Full transcript of audio or video content
            of the product
        VALUE_48: Full cast and credit list For use with dramatized
            audiobooks, filmed entertainment etc, for a cast list sent
            as a separate resource file, not in the ONIX record.
            Equivalent of code 28 in List 153
        VALUE_49: Image for social media Image – not specifically a
            cover image or artwork, contributor image, or logo –
            explicitly intended for use in social media
        VALUE_50: Supplementary learning resources Eg downloadable
            worksheets, home learning materials
        VALUE_51: Cover flap image 2D, front or back flap image
        VALUE_52: Warning label Image of any warning label or hazard
            warning text on product or packaging, eg as required for EU
            General or Toy Safety, or for battery safety purposes
        VALUE_53: Product safety contacts Document giving full contact
            detail, including postal addresses, for product safety
            contacts at publisher or supplier. Deprecated, except for
            use in ONIX 3.0
        VALUE_54: Page edge deco image 2D image of edge decoration (see
            also List 79 code 02)
        VALUE_55: Endpaper deco image 2D image of endpaper (or inside
            front and back cover) decoration (see also List 79 code 55)
        VALUE_99: License Link to a license covering permitted usage of
            the product content. Deprecated in favor of
            &lt;EpubLicense&gt;. This was a temporary workaround in ONIX
            3.0, and use of &lt;EpubLicense&gt; is strongly preferred.
            Not for use in ONIX 3.1 or later
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_56 = "56"
    VALUE_57 = "57"
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
    VALUE_40 = "40"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_44 = "44"
    VALUE_45 = "45"
    VALUE_46 = "46"
    VALUE_47 = "47"
    VALUE_48 = "48"
    VALUE_49 = "49"
    VALUE_50 = "50"
    VALUE_51 = "51"
    VALUE_52 = "52"
    VALUE_53 = "53"
    VALUE_54 = "54"
    VALUE_55 = "55"
    VALUE_99 = "99"
