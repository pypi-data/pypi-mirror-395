from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List27(Enum):
    """
    Subject scheme identifier.

    Attributes:
        VALUE_01: Dewey Dewey Decimal Classification
        VALUE_02: Abridged Dewey
        VALUE_03: LC classification US Library of Congress
            classification
        VALUE_04: LC subject heading US Library of Congress subject
            heading
        VALUE_05: NLM classification US National Library of Medicine
            medical classification
        VALUE_06: MeSH heading US National Library of Medicine Medical
            subject heading
        VALUE_07: NAL subject heading US National Agricultural Library
            subject heading
        VALUE_08: AAT Getty Art and Architecture Thesaurus heading
        VALUE_09: UDC Universal Decimal Classification
        VALUE_10: BISAC Subject Heading BISAC Subject Headings are used
            in the North American market to categorize books based on
            topical content. They serve as a guideline for shelving
            books in physical stores and browsing books in online
            stores. See https://www.bisg.org/complete-bisac-subject-
            headings-list
        VALUE_11: BISAC Regional theme A geographical qualifier used
            with a BISAC subject category
        VALUE_12: BIC subject category Deprecated. The BIC subject
            category scheme is obsolete, see
            https://bic.org.uk/resources/BIC-Standard-Subject-
            Categories/
        VALUE_13: BIC geographical qualifier Deprecated
        VALUE_14: BIC language qualifier (language as subject)
            Deprecated
        VALUE_15: BIC time period qualifier Deprecated
        VALUE_16: BIC educational purpose qualifier Deprecated
        VALUE_17: BIC reading level and special interest qualifier
            Deprecated
        VALUE_18: DDC-Sachgruppen der Deutschen Nationalbibliografie
            Used for German National Bibliography since 2004 (100
            subjects). Is different from value 30. See
            https://www.dnb.de/SharedDocs/Downloads/DE/Professionell/Erschliessen/ddcSachgruppenDNBAb2013.html
            (in German)
        VALUE_19: LC fiction genre heading
        VALUE_20: Keywords For indexing and search purposes, not
            normally intended for display. Where multiple keywords or
            keyword phrases are sent, this should be in a single
            instance of the &lt;SubjectHeadingText&gt; element, and it
            is recommended that they should be separated by semi-colons
            (this is consistent with Library of Congress preferred
            practice)
        VALUE_21: BIC children’s book marketing category See PA/BIC CBMC
            guidelines at https://bic.org.uk/resources/childrens-books-
            marketing-classifications/
        VALUE_22: BISAC Merchandising Theme BISAC Merchandising Themes
            are used in addition to BISAC Subject Headings to denote an
            audience to which a work may be of particular appeal, a time
            of year or event for which a work may be especially
            appropriate, or to further describe fictional works that
            have been subject-coded by genre
        VALUE_23: Publisher’s own category code Which is not in itself a
            subject scheme, but describes other attributes of the
            content, as specified in &lt;SubjectSchemeName&gt;
        VALUE_24: Proprietary subject scheme For example, a publisher’s
            or retailer’s own subject coding scheme. Note that a
            distinctive &lt;SubjectSchemeName&gt; is required with
            proprietary coding schemes
        VALUE_25: Tabla de materias ISBN Latin America
        VALUE_26: Warengruppen-Systematik des deutschen Buchhandels See
            https://vlb.de/assets/images/wgsneuversion2_0.pdf (in
            German)
        VALUE_27: SWD Schlagwortnormdatei – Subject Headings Authority
            File in the German-speaking countries. See
            http://www.dnb.de/standardisierung/normdateien/swd.htm (in
            German) and
            http://www.dnb.de/eng/standardisierung/normdateien/swd.htm
            (English). Deprecated in favor of the GND
        VALUE_28: Thèmes Electre Subject classification used by Electre
            (France)
        VALUE_29: CLIL Classification thématique France. A four-digit
            number, see https://clil.centprod.com/listeActive.html (in
            French)
        VALUE_30: DNB-Sachgruppen Deutsche Bibliothek subject groups.
            Used for German National Bibliography until 2003 (65
            subjects). Is different from value 18. See
            http://www.dnb.de/service/pdf/ddc_wv_alt_neu.pdf (in German)
        VALUE_31: NUGI Nederlandse Uniforme Genre-Indeling (former Dutch
            book trade classification)
        VALUE_32: NUR Nederlandstalige Uniforme Rubrieksindeling (Dutch
            book trade classification, from 2002), see
            http://www.boek.nl/nur (in Dutch)
        VALUE_33: ECPA Christian Book Category Former ECPA Christian
            Product Category Book Codes, consisting of up to three x
            3-letter blocks, for Super Category, Primary Category and
            Sub-Category, previously at
            http://www.ecpa.org/ECPA/cbacategories.xls. No longer
            maintained by the ECPA. Deprecated
        VALUE_34: SISO Schema Indeling Systematische Catalogus Openbare
            Bibliotheken (Dutch library classification)
        VALUE_35: Korean Decimal Classification (KDC) A modified Dewey
            Decimal Classification used in the Republic of Korea
        VALUE_36: DDC Deutsch 22 German Translation of Dewey Decimal
            Classification 22. Also known as DDC 22 ger. See
            http://www.ddc-deutsch.de/produkte/uebersichten/
        VALUE_37: Bokgrupper Norwegian book trade product categories
            (Bokgrupper) administered by the Norwegian Publishers
            Association (http://www.forleggerforeningen.no/)
        VALUE_38: Varegrupper Norwegian bookselling subject categories
            (Bokhandelens varegrupper) administered by the Norwegian
            Booksellers Association (http://bokhandlerforeningen.no/)
        VALUE_39: Læreplaner-KL06 Norwegian school curriculum version.
            Deprecated
        VALUE_40: Nippon Decimal Classification Japanese subject
            classification scheme
        VALUE_41: BSQ BookSelling Qualifier: Russian book trade
            classification
        VALUE_42: ANELE Materias Spain: subject coding scheme of the
            Asociación Nacional de Editores de Libros y Material de
            Enseñanza
        VALUE_43: Utdanningsprogram Codes for Norwegian
            ‘utdanningsprogram’ used in secondary education. See:
            http://www.udir.no/. (Formerly labelled ‘Skolefag’)
        VALUE_44: Programområde Codes for Norwegian ‘programområde’ used
            in secondary education. See http://www.udir.no/. (Formerly
            labelled ‘Videregående’ or ‘Programfag’)
        VALUE_45: Undervisningsmateriell Norwegian list of categories
            for books and other material used in education
        VALUE_46: Norsk DDK Norwegian version of Dewey Decimal
            Classification
        VALUE_47: Varugrupper Swedish bookselling subject categories
        VALUE_48: SAB Swedish classification scheme
        VALUE_49: Läromedelstyp Swedish bookselling educational subject
            type
        VALUE_50: Förhandsbeskrivning Swedish publishers preliminary
            subject classification
        VALUE_51: Spanish ISBN UDC subset Controlled subset of UDC codes
            used by the Spanish ISBN Agency
        VALUE_52: ECI subject categories Subject categories defined by
            El Corte Inglés and used widely in the Spanish book trade
        VALUE_53: Soggetto CCE Classificazione commerciale editoriale
            (Italian book trade subject category based on BIC). CCE
            documentation available at https://www.ie-
            online.it/CCE2_2.0.pdf
        VALUE_54: Qualificatore geografico CCE CCE Geographical
            qualifier
        VALUE_55: Qualificatore di lingua CCE CCE Language qualifier
        VALUE_56: Qualificatore di periodo storico CCE CCE Time Period
            qualifier
        VALUE_57: Qualificatore di livello scolastico CCE CCE
            Educational Purpose qualifier
        VALUE_58: Qualificatore di età di lettura CCE CCE Reading Level
            Qualifier
        VALUE_59: VdS Bildungsmedien Fächer Subject code list of the
            German association of educational media publishers, formerly
            at
            http://www.bildungsmedien.de/service/onixlisten/unterrichtsfach_onix_codelist27_value59_0408.pdf.
            Deprecated – use Thema subject category (eg YPA –
            Educational: Arts, general) instead, and add a Thema
            language qualifier (eg 2ACB – English) for language teaching
        VALUE_60: Fagkoder Norwegian primary and secondary school
            subject categories (fagkoder), see http://www.udir.no/
        VALUE_61: JEL classification Journal of Economic Literature
            classification scheme
        VALUE_62: CSH National Library of Canada subject heading
            (English)
        VALUE_63: RVM Répertoire de vedettes-matière Bibliothèque de
            l’Université Laval) (French)
        VALUE_64: YSA Finnish General Thesaurus (Finnish: Yleinen
            suomalainen asiasanasto). See https://finto.fi/ysa/fi/ (in
            Finnish). Deprecated. No longer updated, and replaced by YSO
            (see code 71)
        VALUE_65: Allärs Swedish translation of the Finnish General
            Thesaurus (Swedish: Allmän tesaurus på svenska). See
            https://finto.fi/allars/sv/ (in Swedish). Deprecated. No
            longer updated, and replaced by YSO (see code 71)
        VALUE_66: YKL Finnish Public Libraries Classification System
            (Finnish: Yleisten kirjastojen luokitusjärjestelmä). See
            https://finto.fi/ykl/fi/ (in Finnish),
            https://finto.fi/ykl/sv/ (in Swedish),
            https://finto.fi/ykl/en/ (in English)
        VALUE_67: MUSA Finnish Music Thesaurus (Finnish: Musiikin
            asiasanasto). See https://finto.fi/musa/fi/ (in Finnish).
            Deprecated, and replaced by YSO (see code 71)
        VALUE_68: CILLA Swedish translation of the Finnish Music
            Thesaurus (Swedish: Specialtesaurus för musik). See
            https://finto.fi/musa/sv/ (in Swedish). Deprecated, and
            replaced by YSO (see code 71)
        VALUE_69: Kaunokki Finnish thesaurus for fiction (Finnish:
            Fiktiivisen aineiston asiasanasto). See
            https://finto.fi/kaunokki/fi/ (in Finnish). Deprecated. No
            longer updated, and replaced by Kauno and SLM (see codes D0
            and D1)
        VALUE_70: Bella Swedish translation of the Finnish thesaurus for
            fiction (Swedish: Specialtesaurus för fiktivt material:).
            See https://finto.fi/kaunokki/sv/ (in Swedish). Deprecated.
            No longer updated, and replaced by Kauno and SLM (see codes
            D0 and D1)
        VALUE_71: YSO General Finnish Ontology (Finnish: Yleinen
            suomalainen ontologia). See https://finto.fi/yso/fi/ (in
            Finnish), https://finto.fi/yso/sv/ (in Swedish),
            https://finto.fi/yso/en/ (in English)
        VALUE_72: PTO Finnish Geospatial Domain Ontology (Finnish:
            Paikkatieto ontologia). See https://finto.fi/pto/fi/ (in
            Finnish), https://finto.fi/pto/sv/ (in Swedish),
            https://finto.fi/pto/en/ (in English)
        VALUE_73: Suomalainen kirja-alan luokitus Finnish book trade
            categorization
        VALUE_74: Sears Sears List of Subject Headings
        VALUE_75: BIC E4L BIC E4Libraries Category Headings, formerly at
            http://www.bic.org.uk/51/E4libraries-Subject-Category-
            Headings/ but replaced by UK Standard Library Categories
            (code 92). Deprecated
        VALUE_76: CSR Code Sujet Rayon: subject categories used by
            bookstores in France
        VALUE_77: Suomalainen oppiaineluokitus Finnish school subject
            categories. See https://www.onixkeskus.fi/media/f/5722
        VALUE_78: Japanese book trade C-Code See
            https://isbn.jpo.or.jp/doc/08.pdf#page=44 (in Japanese)
        VALUE_79: Japanese book trade Genre Code
        VALUE_80: Fiktiivisen aineiston lisäluokitus Finnish fiction
            genre classification. See
            https://finto.fi/ykl/fi/page/fiktioluokka (in Finnish),
            https://finto.fi/ykl/sv/page/fiktioluokka (in Swedish),
            https://finto.fi/ykl/en/page/fiktioluokka (in English)
        VALUE_81: Arabic Subject heading scheme
        VALUE_82: Arabized BIC subject category Arabized version of BIC
            subject category scheme developed by ElKotob.com
        VALUE_83: Arabized LC subject headings Arabized version of
            Library of Congress scheme
        VALUE_84: Bibliotheca Alexandrina Subject Headings
            Classification scheme used by Library of Alexandria
        VALUE_85: Postal code Location defined by postal code. Format is
            two-letter country code (from List 91), space, postal code.
            Note some postal codes themselves contain spaces, eg ‘GB N7
            9DP’ or ‘US 10125’
        VALUE_86: GeoNames ID ID number for geographical place, as
            defined at http://www.geonames.org (eg 2825297 is Stuttgart,
            Germany, see http://www.geonames.org/2825297)
        VALUE_87: NewBooks Subject Classification Used for
            classification of academic and specialist publication in
            German-speaking countries. See http://www.newbooks-
            services.com/de/top/unternehmensportrait/klassifikation-und-
            mapping.html (German) and http://www.newbooks-
            services.com/en/top/about-newbooks/classification-
            mapping.html (English)
        VALUE_88: Chinese Library Classification Subject classification
            maintained by the Editorial Board of Chinese Library
            Classification. See http://cct.nlc.gov.cn for access to
            details of the scheme
        VALUE_89: NTCPDSAC Classification Subject classification for
            Books, Audiovisual products and E-publications formulated by
            China National Technical Committee 505
        VALUE_90: Season and Event Indicator German code scheme
            indicating association with seasons, holidays, events (eg
            Autumn, Back to School, Easter)
        VALUE_91: GND (de: Gemeinsame Normdatei) Integrated Authority
            File used in the German-speaking countries. See
            https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html
            (German) and
            https://www.dnb.de/EN/Professionell/Standardisierung/GND/gnd_node.html
            (English). Combines the PND, SWD and GKD into a single
            authority file, and should be used in preference to the
            older codes
        VALUE_92: BIC UKSLC UK Standard Library Categories, the
            successor to BIC’s E4L classification scheme. See
            https://bic.org.uk/resources/uk-standard-library-categories/
        VALUE_93: Thema subject category International multilingual
            subject category scheme – see https://ns.editeur.org/thema
        VALUE_94: Thema place qualifier
        VALUE_95: Thema language qualifier
        VALUE_96: Thema time period qualifier
        VALUE_97: Thema educational purpose qualifier
        VALUE_98: Thema interest age / special interest qualifier
        VALUE_99: Thema style qualifier
        A2: Ämnesord Swedish subject categories maintained by
            Bokrondellen
        A3: Statystyka Książek Papierowych, Mówionych I Elektronicznych
            Polish Statistical Book and E-book Classification
        A4: CCSS Common Core State Standards curriculum alignment, for
            links to US educational standards. &lt;SubjectCode&gt; uses
            the full dot notation. See
            http://www.corestandards.org/developers-and-publishers
        A5: Rameau French library subject headings
        A6: Nomenclature discipline scolaire French educational subject
            classification, URI
            http://data.education.fr/voc/scolomfr/scolomfr-voc-015GTPX
        A7: ISIC International Standard Industry Classification, a
            classification of economic activities. Use for books that
            are about a particular industry or economic activity.
            &lt;SubjectCode&gt; should be a single letter denoting an
            ISIC section OR a 2-, 3- or 4-digit number denoting an ISIC
            division, group or class. See
            http://unstats.un.org/unsd/cr/registry/isic-4.asp
        A8: LC Children’s Subject Headings Library of Congress
            Children’s Subject Headings: LCSHAC supplementary headings
            for Children’s books
        A9: Ny Läromedel Swedish bookselling educational subject
        B0: EuroVoc EuroVoc multilingual thesaurus. &lt;SubjectCode&gt;
            should be a EuroVoc concept dc:identifier (for example,
            2777, ‘refrigerated products’). See http://eurovoc.europa.eu
        B1: BISG Educational Taxonomy Controlled vocabulary for
            educational objectives. See
            https://www.bisg.org/products/recommendations-for-citing-
            educational-standards-and-objectives-in-metadata
        B2: Keywords (not for display) For indexing and search purposes,
            MUST not be displayed. Where multiple keywords or keyword
            phrases are sent, this should be in a single instance of the
            &lt;SubjectHeadingText&gt; element, and it is recommended
            that they should be separated by semi-colons. Use of code B2
            should be very rare: use B2 in preference to code 20 only
            where it is important to show the keyword list is
            specifically NOT for display to purchasers (eg some keywords
            for a medical textbook may appear offensive if displayed out
            of context)
        B3: Nomenclature Diplôme French higher and vocational
            educational subject classification, URI
            http://data.education.fr/voc/scolomfr/scolomfr-voc-029
        B4: Key character names For fiction and non-fiction, one or more
            key names, provided – like keywords – for indexing and
            search purposes. Where multiple character names are sent,
            this should be in a single instance of
            &lt;SubjectHeadingText&gt;, and multiple names should be
            separated by semi-colons. Note &lt;NameAsSubject&gt; should
            be used for people who are the central subject of the book.
            Code B4 may be used for names of lesser importance
        B5: Key place names For fiction and non-fiction, one or more key
            names, provided – like keywords – for indexing and search
            purposes. Where multiple place names are sent, this should
            in a single instance of &lt;SubjectHeadingText&gt;, and
            multiple names should be separated by semi-colons. Only for
            use in ONIX 3.0 or later
        B6: FAST Faceted Application of Subject Terminology, OCLC
            subject scheme derived from LCSH (see code 04). See
            https://fast.oclc.org/fast/. Codes are up to 8 digits, for
            example 1726640 for Historical fiction (see
            https://id.worldcat.org/fast/1726640). Only for use in ONIX
            3.0 or later
        B7: NGSS Next Generation Science Standards for K-12 education in
            the USA (https://www.nextgenscience.org).
            &lt;SubjectCode&gt; is a code such as 4-PS3-2. Only for use
            in ONIX 3.0 or later
        B8: MVB-Lesemotive MVB classification of ‘reading rationales’,
            which classify unconscious motives that lead to a book
            purchase. Categories are assigned and maintained by MVB.
            Only for use in ONIX 3.0 or later. See
            https://vlb.de/lesemotive
        B9: LOPS21 Subject module Finnish Suomalainen oppiaineluokitus.
            Only for use in ONIX 3.0 or later
        C0: Læreplaner-LK20 Codes for Norwegian curriculum for primary
            and secondary education. Only for use in ONIX 3.0 or later.
            See Læreplaner-LK20 at https://www.udir.no/om-
            udir/data/kl06-grep/
        C1: Kompetansemål-LK20 Codes for competency aims in the
            Norwegian curriculum for primary and secondary education.
            Only for use in ONIX 3.0 or later. See Kompetansemål-LK20 at
            https://www.udir.no/om-udir/data/kl06-grep/
        C2: Kompetansemålsett-LK20 Codes for sets of competency aims in
            the Norwegian curriculum for primary and secondary
            education. Only for use in ONIX 3.0 or later. See
            Kompetansemålsett-LK20 at https://www.udir.no/om-
            udir/data/kl06-grep/
        C3: Tverrfaglige temaer-LK20 Codes for interdisciplinary topics
            in the Norwegian curriculum for primary and secondary
            education. Only for use in ONIX 3.0 or later. See
            Tverrfaglige temaer-LK20 at https://www.udir.no/om-
            udir/data/kl06-grep/
        C4: CLIL – Type d’article scolaire Only for use in ONIX 3.0 or
            later
        C5: GAR – Type pédagogique Gestionnaire d’Accès aux resources –
            see https://gar.education.fr/ Only for use in ONIX 3.0 or
            later
        C6: ISCED-F UNESCO ISCED Fields of education and training
            (2013), eg &lt;SubjectCode&gt; 0222 is ‘History and
            archaeology’. Only for use in ONIX 3.0 or later. See
            http://uis.unesco.org/sites/default/files/documents/international-
            standard-classification-of-education-fields-of-education-
            and-training-2013-detailed-field-descriptions-2015-en.pdf
        C7: Klassifikationen von Spielen, Puzzles und Spielwaren German
            category scheme for games, puzzles and toys. Only for use in
            ONIX 3.0 or later. See
            https://www.ludologie.de/fileadmin/user_upload/PDFs/211126_Kategorisierung_von_Spielen_Puzzles_und_Spielwaren.pdf
        C8: NBVok NTSF National Library of Norway genre and form
            thesaurus. Only for use in ONIX 3.0 or later. See
            https://www.nb.no/nbvok/ntsf
        C9: JPRO Genre Subject / genre code used in Japan. Only for use
            in ONIX 3.0 or later
        D0: KAUNO Finnish Ontology for fiction (Finnish: Fiktiivisen
            aineiston ontologia). See https://finto.fi/kauno/fi/ (in
            Finnish), https://finto.fi/kauno/sv/ (in Swedish),
            https://finto.fi/kauno/en/ (in English). Only for use in
            ONIX 3.0 or later
        D1: SLM Finnish genre and form vocabulary (Finnish: Suomalainen
            lajityyppi ja muotosanasto). See https://finto.fi/slm/fi/
            (in Finnish), https://finto.fi/slm/sv/ (in Swedish),
            https://finto.fi/slm/en/ (in English). Only for use in ONIX
            3.0 or later
        D2: YSO-places General Finnish Ontology for Places (Finnish:
            Yleinen suomalainen ontologia – paikat). See
            https://finto.fi/yso-paikat/fi/ (in Finnish),
            https://finto.fi/yso-paikat/sv/ (in Swedish),
            https://finto.fi/yso-paikat/en/ (in English). Only for use
            in ONIX 3.0 or later
        D3: Norske emneord See https://www.nb.no/nbvok/nb/. Only for use
            in ONIX 3.0 or later
        D4: Austlang Controlled vocabulary and alphanumeric codes for
            Aboriginal and Torres Strait Islander languages and peoples,
            maintained by the Australian Institute of Aboriginal and
            Torres Strait Islander Studies (AIATSIS), for use where the
            book is about a language or the people that traditionally
            speak it. Only for use in ONIX 3.0 or later. See
            https://collection.aiatsis.gov.au/austlang
        D5: German Tropes list Only for use in ONIX 3.0 or later
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
    VALUE_56 = "56"
    VALUE_57 = "57"
    VALUE_58 = "58"
    VALUE_59 = "59"
    VALUE_60 = "60"
    VALUE_61 = "61"
    VALUE_62 = "62"
    VALUE_63 = "63"
    VALUE_64 = "64"
    VALUE_65 = "65"
    VALUE_66 = "66"
    VALUE_67 = "67"
    VALUE_68 = "68"
    VALUE_69 = "69"
    VALUE_70 = "70"
    VALUE_71 = "71"
    VALUE_72 = "72"
    VALUE_73 = "73"
    VALUE_74 = "74"
    VALUE_75 = "75"
    VALUE_76 = "76"
    VALUE_77 = "77"
    VALUE_78 = "78"
    VALUE_79 = "79"
    VALUE_80 = "80"
    VALUE_81 = "81"
    VALUE_82 = "82"
    VALUE_83 = "83"
    VALUE_84 = "84"
    VALUE_85 = "85"
    VALUE_86 = "86"
    VALUE_87 = "87"
    VALUE_88 = "88"
    VALUE_89 = "89"
    VALUE_90 = "90"
    VALUE_91 = "91"
    VALUE_92 = "92"
    VALUE_93 = "93"
    VALUE_94 = "94"
    VALUE_95 = "95"
    VALUE_96 = "96"
    VALUE_97 = "97"
    VALUE_98 = "98"
    VALUE_99 = "99"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"
    A6 = "A6"
    A7 = "A7"
    A8 = "A8"
    A9 = "A9"
    B0 = "B0"
    B1 = "B1"
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"
    B5 = "B5"
    B6 = "B6"
    B7 = "B7"
    B8 = "B8"
    B9 = "B9"
    C0 = "C0"
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    C5 = "C5"
    C6 = "C6"
    C7 = "C7"
    C8 = "C8"
    C9 = "C9"
    D0 = "D0"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"
    D5 = "D5"
