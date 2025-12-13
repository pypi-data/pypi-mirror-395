from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List73(Enum):
    """
    Website role.

    Attributes:
        VALUE_00: Unspecified, see website description
        VALUE_01: Publisher’s corporate website See also codes 17 and 18
        VALUE_02: Publisher’s website for a specified work A publisher’s
            informative and/or promotional webpage relating to a
            specified work (book, journal, online resource or other
            publication type)
        VALUE_03: Online hosting service home page A webpage giving
            access to an online content hosting service as a whole
        VALUE_04: Journal home page A webpage giving general information
            about a serial, in print or electronic format or both
        VALUE_05: Online resource ‘available content’ page A webpage
            giving direct access to the content that is available online
            for a specified resource version. Generally used for content
            available online under subscription terms
        VALUE_06: Contributor’s own website A webpage maintained by an
            author or other contributor about their publications and
            personal background
        VALUE_07: Publisher’s website relating to specified contributor
            A publisher’s webpage devoted to a specific author or other
            contributor
        VALUE_08: Other publisher’s website relating to specified
            contributor A webpage devoted to a specific author or other
            contributor, and maintained by a publisher other than the
            publisher of the item described in the ONIX record
        VALUE_09: Third-party website relating to specified contributor
            A webpage devoted to a specific author or other contributor,
            and maintained by a third party (eg a fan site)
        VALUE_10: Contributor’s own website for specified work A webpage
            maintained by an author or other contributor and specific to
            an individual work
        VALUE_11: Other publisher’s website relating to specified work A
            webpage devoted to an individual work, and maintained by a
            publisher other than the publisher of the item described in
            the ONIX record
        VALUE_12: Third-party website relating to specified work A
            webpage devoted to an individual work, and maintained by a
            third party (eg a fan site)
        VALUE_13: Contributor’s own website for group or series of works
            A webpage maintained by an author or other contributor and
            specific to a group or series of works
        VALUE_14: Publisher’s website relating to group or series of
            works A publisher’s webpage devoted to a group or series of
            works
        VALUE_15: Other publisher’s website relating to group or series
            of works A webpage devoted to a group or series of works,
            and maintained by a publisher other than the publisher of
            the item described in the ONIX record
        VALUE_16: Third-party website relating to group or series of
            works (eg a fan site) A webpage devoted to a group or series
            of works, and maintained by a third party (eg a fan site)
        VALUE_17: Publisher’s B2B website Use instead of code 01 to
            specify a publisher’s website for trade users
        VALUE_18: Publisher’s B2C website Use instead of code 01 to
            specify a publisher’s website for end customers (consumers)
        VALUE_23: Author blog For example, a Blogger or Tumblr URL, a
            Wordpress website or other blog URL
        VALUE_24: Web page for author presentation / commentary
        VALUE_25: Web page for author interview
        VALUE_26: Web page for author reading
        VALUE_27: Web page for cover material
        VALUE_28: Web page for sample content
        VALUE_29: Web page for full content Use this value in the
            &lt;Website&gt; composite (typically within
            &lt;Publisher&gt; or &lt;SupplyDetail&gt;) when sending a
            link to a webpage at which a digital product is available
            for download and/or online access
        VALUE_30: Web page for other commentary / discussion For example
            a subscribable podcast hosting site, social media message,
            newsletter issue, other commentary
        VALUE_31: Transfer-URL URL needed by the German National Library
            for direct access, harvesting and storage of an electronic
            resource
        VALUE_32: DOI Website Link Link needed by German Books in Print
            (VLB) for DOI registration and ONIX DOI conversion
        VALUE_33: Supplier’s corporate website A corporate website
            operated by a distributor or other supplier (not the
            publisher)
        VALUE_34: Supplier’s B2B website A website operated by a
            distributor or other supplier (not the publisher) and aimed
            at trade customers
        VALUE_35: Supplier’s B2C website A website operated by a
            distributor or other supplier (not the publisher) and aimed
            at consumers
        VALUE_36: Supplier’s website for a specified work A distributor
            or supplier’s webpage describing a specified work
        VALUE_37: Supplier’s B2B website for a specified work A
            distributor or supplier’s webpage describing a specified
            work, and aimed at trade customers
        VALUE_38: Supplier’s B2C website for a specified work A
            distributor or supplier’s webpage describing a specified
            work, and aimed at consumers
        VALUE_39: Supplier’s website for a group or series of works A
            distributor or supplier’s webpage describing a group or
            series of works
        VALUE_40: URL of full metadata description For example an ONIX
            or MARC record for the product, available online
        VALUE_41: Social networking URL for specific work or product For
            example, a Facebook, Instagram, Youtube, Pinterest, Tiktok
            (including Booktok), Twitter (latterly, X) or similar URL
            for the product or work
        VALUE_42: Author’s social networking URL For example, a
            Facebook, Instagram, Youtube, Pinterest, Tiktok (including
            Booktok), Twitter (latterly, X) or similar page for the
            contributor
        VALUE_43: Publisher’s social networking URL For example, a
            Facebook, Instagram, Youtube, Pinterest, Tiktok (including
            Booktok), Twitter (latterly, X) or similar page
        VALUE_44: Social networking URL for specific article, chapter or
            content item For example, a Facebook, Instagram, Youtube,
            Pinterest, Tiktok (including Booktok), Twitter (latterly, X)
            or similar page. Use only in the context of a specific
            content item (eg within &lt;ContentItem&gt;)
        VALUE_45: Publisher’s or third party website for permissions
            requests For example, a service offering click-through
            licensing of extracts
        VALUE_46: Publisher’s or third party website for privacy
            statement For example, a page providing details related to
            GDPR. Only for use in ONIX 3.0 or later
        VALUE_47: Publisher’s website for digital preservation The URL
            of the publisher’s preservation service, or a more specific
            URL for access to its preservation metadata, to provide
            confirmation of the preservation status of the product.
            &lt;WebsiteDescription&gt; may contain the name of the
            service. Only for use in ONIX 3.0 or later
        VALUE_48: Third-party website for digital preservation The URL
            of the preservation service (eg https://clockss.org), or a
            more specific URL for access to its preservation metadata,
            to provide confirmation of the preservation status of the
            product. &lt;WebsiteDescription&gt; may contain the name of
            the service. Only for use in ONIX 3.0 or later
        VALUE_49: Product website for environmental responsibility
            statement The URL of a web page describing the environmental
            and sustainability policy, or carbon neutrality status, that
            applies to the specific product. Only for use in ONIX 3.0 or
            later
        VALUE_50: Organization’s website for environmental
            responsibility statement The URL of a web page describing
            the environmental and sustainability policies, carbon
            neutrality status, etc of the organization (publisher,
            supplier etc). For environmental sustainability of the
            product itself, see List 79. Only for use in ONIX 3.0 or
            later
        VALUE_51: Legal deposit website for digital preservation The URL
            of a digital legal deposit service (eg
            https://www.legaldeposit.org.uk), or a more specific URL for
            access to its preservation metadata, to provide confirmation
            of the digital legal deposit status of the product.
            &lt;WebsiteDescription&gt; may contain the name of the
            service. Only for use in ONIX 3.0 or later
        VALUE_52: Publisher’s or third party contact form For example, a
            web page providing an interactive contact form for safety-
            related issues. Only for use in ONIX 3.0 or later
        VALUE_53: Organization’s website for corporate social
            responsibility The URL of a web page describing the CSR
            policies, including corporate ethics, governance and human
            rights or modern slavery statements, of the organization,
            but see code 50 for sustainability. Only for use in ONIX 3.0
            or later
        VALUE_54: Website for Indigenous statement or resource The URL
            of a web page providing a statement, protocol or resource
            relevant to indigenous publishing. This may include content
            hosted by the publisher, a contributor, or a third party.
            Examples include Reconciliation Action Plans (RAPs),
            Indigenous Cultural and Intellectual Property (ICIP)
            acknowledgements, cultural protocols, author guidelines,
            nation, community, or language resources, or contextual
            references such as Indigenous place names, territories, or
            treaties (eg native-land.ca). May be used at either
            organisational or product level, and additional specifics
            about the web page should be provided using
            &lt;WebsiteDescription&gt;. Only for use in ONIX 3.0 or
            later
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
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
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
