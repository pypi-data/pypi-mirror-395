from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List145(Enum):
    """
    Usage type.

    Attributes:
        VALUE_00: No constraints Allows positive indication that there
            are no particular constraints (that can be specified in
            &lt;EpubUsageConstraint&gt;). By convention, use 01 in
            &lt;EpubUsageStatus&gt;
        VALUE_01: Preview Preview before purchase. Allows a retail
            customer, account holder or patron to view or listen to a
            proportion of the book before purchase. Also applies to
            borrowers making use of ‘acquisition on demand’ models in
            libraries, and to ‘subscription’ models where the purchase
            is made on behalf of the reader. Note that any Sales embargo
            date (in &lt;PublishingDate&gt; or &lt;MarketDate&gt;) also
            applies to provision of previews, unless an explicit date is
            provided for the preview
        VALUE_02: Print Make physical copy of extract
        VALUE_03: Copy / paste Make digital copy of extract
        VALUE_04: Share Share product across multiple concurrent
            devices. Allows a retail customer, account holder or patron
            to read the book across multiple devices linked to the same
            account. Also applies to readers in library borrowing and
            ‘subscription’ models
        VALUE_05: Text to speech ‘Read aloud’ with text to speech
            functionality
        VALUE_06: Lend Lendable by the purchaser to another device owner
            or account holder or patron, eg ‘Lend-to-a-friend’, or
            library lending (where the library product has a separate
            &lt;ProductIdentifier&gt; from the consumer product – but
            for this prefer code 16). The ‘primary’ copy becomes
            unusable while the secondary copy is ‘lent’ unless a number
            of concurrent borrowers is also specified
        VALUE_07: Time-limited license E-publication license is time-
            limited. Use with code 02 from List 146 and either a time
            period in days, weeks or months in &lt;EpubUsageLimit&gt;,
            or a Valid until date in &lt;EpubUsageLimit&gt;. The
            purchased copy becomes unusable when the license expires.
            For clarity, a perpetual license is the default, but may be
            specified explicitly with code 01 from list 146, or with
            code 02 and a limit &lt;Quantity&gt; of 0 days
        VALUE_08: Library loan renewal Maximum number of consecutive
            loans or loan extensions (usually from a library) to a
            single device owner or account holder or patron. Note that a
            limit of 1 indicates that a loan cannot be renewed or
            extended
        VALUE_09: Multi-user license E-publication license is multi-
            user. Maximum number of concurrent users licensed to use the
            product should be given in &lt;EpubUsageLimit&gt;. For
            clarity, unlimited concurrency is the default, but may be
            specified explicitly with code 01 from list 146, or with
            code 02 and a limit &lt;Quantity&gt; of 0 users
        VALUE_10: Preview on premises Preview locally before purchase.
            Allows a retail customer, account holder or patron to view a
            proportion of the book (or the whole book, if no proportion
            is specified) before purchase, but ONLY while located
            physically in the retailer’s store (eg while logged on to
            the store or library wifi). Also applies to patrons making
            use of ‘acquisition on demand’ models in libraries
        VALUE_11: Text and data mining Make use of the content of the
            product (text, images, audio etc) or the product metadata or
            supporting resources for extraction of useful (and possibly
            new) information through automated computer analysis, or for
            training of tools for such analysis (including training of
            generative AI models). By convention, use 01 or 03 in
            &lt;EpubUsageStatus&gt;. Note 03 should be regarded as
            ‘prohibited to the full extent allowed by law’, or otherwise
            expressly reserved by the rightsholder, as in some
            jurisdictions, TDM may be subject to copyright exception (eg
            for not-for-profit purposes), subject to optional
            reservation, or allowed under ‘fair use’ doctrine
        VALUE_16: Library loan Loanable by the purchaser (usually a
            library) to other device owner or account holder or patron,
            eg library lending (whether or not the library product has a
            separate &lt;ProductIdentifier&gt; from the consumer
            product). The ‘primary’ copy becomes unusable while the
            secondary copy is ‘on loan’ unless a number of concurrent
            borrowers is also specified. Use code 08 to specify any
            limit on loan renewals
    """

    VALUE_00 = "00"
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
    VALUE_16 = "16"
