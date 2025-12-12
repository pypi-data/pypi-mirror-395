from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List96(Enum):
    """
    Currency code – based on ISO 4217.

    Attributes:
        AED: UAE Dirham United Arab Emirates
        AFA: Afghani Afghanistan. Deprecated, replaced by AFN
        AFN: Afghani Afghanistan (prices normally quoted as integers)
        ALL: Lek Albania (prices normally quoted as integers)
        AMD: Armenian Dram Armenia (prices normally quoted as integers)
        ANG: Netherlands Antillean Guilder Curaçao, Sint Maarten.
            Replaced by the Caribbean Guilder (XCG) from April 2025.
            Deprecated – use only for historical prices that pre-date
            withdrawal
        AOA: Kwanza Angola
        ARS: Argentine Peso Argentina
        ATS: Schilling Austria. Now replaced by the Euro (EUR).
            Deprecated – use only for historical prices that pre-date
            the introduction of the Euro
        AUD: Australian Dollar Australia, Christmas Island, Cocos
            (Keeling) Islands, Heard Island and McDonald Islands,
            Kiribati, Nauru, Norfolk Island, Tuvalu
        AWG: Aruban Florin Aruba
        AZN: Azerbaijan Manat Azerbaijan
        BAM: Convertible Marks Bosnia and Herzegovina
        BBD: Barbados Dollar Barbados
        BDT: Taka Bangladesh
        BEF: Belgian Franc Belgium. Now replaced by the Euro (EUR).
            Deprecated – use only for historical prices that pre-date
            the introduction of the Euro
        BGL: Bulgarian Lev Deprecated, replaced by BGN
        BGN: Bulgarian Lev Bulgaria
        BHD: Bahraini Dinar Bahrain (prices normally quoted with 3
            decimal places)
        BIF: Burundi Franc Burundi (prices normally quoted as integers)
        BMD: Bermudian Dollar Bermuda
        BND: Brunei Dollar Brunei Darussalam
        BOB: Boliviano Bolivia
        BRL: Brazilian Real Brazil
        BSD: Bahamian Dollar Bahamas
        BTN: Ngultrun Bhutan
        BWP: Pula Botswana
        BYR: (Old) Belarussian Ruble Belarus (prices normally quoted as
            integers). Deprecated – now replaced by new Belarussian
            Ruble (BYN): use only for historical prices that pre-date
            the introduction of the new Belarussian Ruble
        BYN: Belarussian Ruble Belarus
        BZD: Belize Dollar Belize
        CAD: Canadian Dollar Canada
        CDF: Franc Congolais Congo (Democratic Republic of the)
        CHF: Swiss Franc Switzerland, Liechtenstein
        CLP: Chilean Peso Chile (prices normally quoted as integers)
        CNY: Yuan Renminbi China
        COP: Colombian Peso Colombia (prices normally quoted as
            integers)
        CRC: Costa Rican Colon Costa Rica (prices normally quoted as
            integers)
        CSD: Serbian Dinar Deprecated, replaced by RSD
        CUC: Cuban Convertible Peso Cuba (alternative currency from
            1994, withdrawn 2021). Deprecated – use only for historical
            prices that pre-date withdrawal
        CUP: Cuban Peso Cuba
        CVE: Cabo Verde Escudo Cabo Verde (prices normally quoted as
            integers)
        CYP: Cyprus Pound Cyprus. Now replaced by the Euro (EUR).
            Deprecated – use only for historical prices that pre-date
            the introduction of the Euro
        CZK: Czech Koruna Czechia
        DEM: Mark Germany. Now replaced by the Euro (EUR). Deprecated –
            use only for historical prices that pre-date the
            introduction of the Euro
        DJF: Djibouti Franc Djibouti (prices normally quoted as
            integers)
        DKK: Danish Krone Denmark, Faroe Islands, Greenland
        DOP: Dominican Peso Dominican Republic
        DZD: Algerian Dinar Algeria
        EEK: Kroon Estonia. Now replaced by the Euro (EUR). Deprecated –
            use only for historical prices that pre-date the
            introduction of the Euro
        EGP: Egyptian Pound Egypt
        ERN: Nakfa Eritrea
        ESP: Peseta Spain. Now replaced by the Euro (EUR). Deprecated –
            use only for historical prices that pre-date the
            introduction of the Euro (prices normally quoted as
            integers)
        ETB: Ethiopian Birr Ethiopia
        EUR: Euro Eurozone: Andorra, Austria, Belgium, Croatia, Cyprus,
            Estonia, Finland, France, Fr Guiana, Fr S Territories,
            Germany, Greece, Guadeloupe, Holy See (Vatican City),
            Ireland, Italy, Latvia, Lithuania, Luxembourg, Martinique,
            Malta, Mayotte, Monaco, Montenegro, Netherlands, Portugal,
            Réunion, St Barthelemy, St Martin, St Pierre and Miquelon,
            San Marino, Slovakia, Slovenia, Spain
        FIM: Markka Finland. Now replaced by the Euro (EUR). Deprecated
            – use only for historical prices that pre-date the
            introduction of the Euro
        FJD: Fiji Dollar Fiji
        FKP: Falkland Islands Pound Falkland Islands (Malvinas)
        FRF: Franc France. Now replaced by the Euro (EUR). Deprecated –
            use only for historical prices that pre-date the
            introduction of the Euro
        GBP: Pound Sterling United Kingdom, Isle of Man, Channel
            Islands, South Georgia, South Sandwich Islands, British
            Indian Ocean Territory (de jure)
        GEL: Lari Georgia
        GHC: Ghana Cedi Deprecated, replaced by GHS
        GHS: Ghana Cedi Ghana
        GIP: Gibraltar Pound Gibraltar
        GMD: Dalasi Gambia
        GNF: Guinean Franc Guinea (prices normally quoted as integers)
        GRD: Drachma Greece. Now replaced by the Euro (EUR). Deprecated
            – use only for historical prices that pre-date the
            introduction of the Euro
        GTQ: Quetzal Guatemala
        GWP: Guinea-Bissau Peso Now replaced by the CFA Franc BCEAO XOF
            use only for historical prices that pre-date use of the CFA
            Franc
        GYD: Guyana Dollar Guyana (prices normally quoted as integers)
        HKD: Hong Kong Dollar Hong Kong
        HNL: Lempira Honduras
        HRK: Kuna Croatia. Now replaced by the Euro (EUR). Deprecated –
            use only for historical prices that pre-date the
            introduction of the Euro
        HTG: Gourde Haiti
        HUF: Forint Hungary (prices normally quoted as integers)
        IDR: Rupiah Indonesia (prices normally quoted as integers)
        IEP: Punt Ireland. Now replaced by the Euro (EUR). Deprecated –
            use only for historical prices that pre-date the
            introduction of the Euro
        ILS: New Israeli Sheqel Israel
        INR: Indian Rupee India, Bhutan (prices normally quoted as
            integers)
        IQD: Iraqi Dinar Iraq (prices normally quoted as integers)
        IRR: Iranian Rial Iran (Islamic Republic of) (prices normally
            quoted as integers)
        ISK: Iceland Krona Iceland (prices normally quoted as integers)
        ITL: Lira Italy. Now replaced by the Euro (EUR). Deprecated –
            use only for historical prices that pre-date the
            introduction of the Euro (prices normally quoted as
            integers)
        JMD: Jamaican Dollar Jamaica
        JOD: Jordanian Dinar Jordan (prices normally quoted with 3
            decimal places)
        JPY: Yen Japan (prices normally quoted as integers)
        KES: Kenyan Shilling Kenya
        KGS: Som Kyrgyzstan
        KHR: Riel Cambodia
        KMF: Comorian Franc Comoros (prices normally quoted as integers)
        KPW: North Korean Won Korea (Democratic People’s Republic of)
            (prices normally quoted as integers)
        KRW: Won Korea (Republic of) (prices normally quoted as
            integers)
        KWD: Kuwaiti Dinar Kuwait (prices normally quoted with 3 decimal
            places)
        KYD: Cayman Islands Dollar Cayman Islands
        KZT: Tenge Kazakhstan
        LAK: Lao Kip Lao People’s Democratic Republic (prices normally
            quoted as integers)
        LBP: Lebanese Pound Lebanon (prices normally quoted as integers)
        LKR: Sri Lanka Rupee Sri Lanka
        LRD: Liberian Dollar Liberia
        LSL: Loti Lesotho
        LTL: Litus Lithuania. Now replaced by the Euro (EUR). Deprecated
            – use only for historical prices that pre-date the
            introduction of the Euro
        LUF: Luxembourg Franc Luxembourg. Now replaced by the Euro
            (EUR). Deprecated – use only for historical prices that pre-
            date the introduction of the Euro (prices normally quoted as
            integers)
        LVL: Latvian Lats Latvia. Now replaced by the Euro (EUR).
            Deprecated – use only for historical prices that pre-date
            the introduction of the Euro
        LYD: Libyan Dinar Libyan Arab Jamahiriya (prices normally quoted
            with 3 decimal places)
        MAD: Moroccan Dirham Morocco, Western Sahara
        MDL: Moldovan Leu Moldova, Republic of
        MGA: Malagasy Ariary Madagascar (prices normally quoted with 0
            or 1 decimal place – 1 iraimbilanja = Ar0.2)
        MGF: Malagasy Franc Now replaced by the Ariary (MGA) (prices
            normally quoted as integers)
        MKD: Denar North Macedonia (formerly FYR Macedonia)
        MMK: Kyat Myanmar (prices normally quoted as integers)
        MNT: Tugrik Mongolia (prices normally quoted as integers)
        MOP: Pataca Macau
        MRO: (Old) Ouguiya Mauritania (prices normally quoted with 0 or
            1 decimal place – 1 khoums = UM0.2). Was interchangeable
            with MRU (New) Ouguiya at rate of 10:1 until June 2018.
            Deprecated, use MRU instead
        MRU: Ouguiya Mauritania (prices normally quoted with 0 or 1
            decimal place – 1 khoums = UM0.2). Replaced MRO (old)
            Ouguiya at rate of 10:1 in June 2018. Only for use in ONIX
            3.0 or later
        MTL: Maltese Lira Malta. Now replaced by the Euro (EUR).
            Deprecated – use only for historical prices that pre-date
            the introduction of the Euro
        MUR: Mauritius Rupee Mauritius (prices normally quoted as
            integers)
        MVR: Rufiyaa Maldives
        MWK: Malawi Kwacha Malawi
        MXN: Mexican Peso Mexico
        MYR: Malaysian Ringgit Malaysia
        MZN: Mozambique Metical Mozambique
        NAD: Namibia Dollar Namibia
        NGN: Naira Nigeria
        NIO: Cordoba Oro Nicaragua
        NLG: Guilder Netherlands. Now replaced by the Euro (EUR).
            Deprecated – use only for historical prices that pre-date
            the introduction of the Euro
        NOK: Norwegian Krone Norway, Bouvet Island, Svalbard and Jan
            Mayen
        NPR: Nepalese Rupee Nepal
        NZD: New Zealand Dollar New Zealand, Cook Islands, Niue,
            Pitcairn, Tokelau
        OMR: Rial Omani Oman (prices normally quoted with 3 decimal
            places)
        PAB: Balboa Panama
        PEN: Sol Peru (formerly Nuevo Sol)
        PGK: Kina Papua New Guinea
        PHP: Philippine Peso Philippines
        PKR: Pakistan Rupee Pakistan (prices normally quoted as
            integers)
        PLN: Złoty Poland
        PTE: Escudo Portugal. Now replaced by the Euro (EUR). Deprecated
            – use only for historical prices that pre-date the
            introduction of the Euro
        PYG: Guarani Paraguay (prices normally quoted as integers)
        QAR: Qatari Rial Qatar
        ROL: Romanian Old Leu Deprecated, replaced by RON
        RON: Romanian Leu Romania
        RSD: Serbian Dinar Serbia (prices normally quoted as integers)
        RUB: Russian Ruble Russian Federation
        RUR: Russian Ruble Deprecated, replaced by RUB
        RWF: Rwanda Franc Rwanda (prices normally quoted as integers)
        SAR: Saudi Riyal Saudi Arabia
        SBD: Solomon Islands Dollar Solomon Islands
        SCR: Seychelles Rupee Seychelles
        SDD: Sudanese Dinar Now replaced by the Sudanese Pound (SDG)
        SDG: Sudanese Pound Sudan
        SEK: Swedish Krona Sweden
        SGD: Singapore Dollar Singapore
        SHP: Saint Helena Pound Saint Helena
        SIT: Tolar Slovenia. Now replaced by the Euro (EUR). Deprecated
            – use only for historical prices that pre-date the
            introduction of the Euro
        SKK: Slovak Koruna Slovakia. Now replaced by the Euro (EUR).
            Deprecated – use only for historical prices that pre-date
            the introduction of the Euro
        SLE: Leone Sierra Leone (from April 2022). Only for use in ONIX
            3.0 or later
        SLL: Leone Sierra Leone (prices normally quoted as integers).
            Deprecated – gradually replaced by SLE from April 2022, but
            SLL Leone still usable until December 2023 (SLE is a
            redenomination of the Leone by a factor of 1,000)
        SOS: Somali Shilling Somalia (prices normally quoted as
            integers)
        SRD: Surinam Dollar Suriname
        SRG: Suriname Guilder DEPRECATED, replaced by SRD
        STD: (Old) Dobra São Tome and Principe (prices normally quoted
            as integers). Was interchangeable with STN (New) Dobra at
            rate of 1000:1 until June 2018. Deprecated, use STN instead
        STN: Dobra São Tome and Principe. Replaced STD (old) Dobra at
            rate of 1000:1 in June 2018. Only for use in ONIX 3.0 or
            later
        SVC: El Salvador Colon El Salvador
        SYP: Syrian Pound Syrian Arab Republic (prices normally quoted
            as integers)
        SZL: Lilangeni Eswatini (formerly known as Swaziland)
        THB: Baht Thailand
        TJS: Somoni Tajikistan
        TMM: Turkmenistan Manat Deprecated, replaced by TMT (prices
            normally quoted as integers)
        TMT: Turkmenistan New Manat Turkmenistan
        TND: Tunisian Dinar Tunisia (prices normally quoted with 3
            decimal places)
        TOP: Pa’anga Tonga
        TPE: Timor Escudo Deprecated. Timor-Leste now uses the US Dollar
        TRL: Turkish Lira (old) Deprecated, replaced by TRY (prices
            normally quoted as integers)
        TRY: Turkish Lira Türkiye, from 1 January 2005
        TTD: Trinidad and Tobago Dollar Trinidad and Tobago
        TWD: New Taiwan Dollar Taiwan (Province of China)
        TZS: Tanzanian Shilling Tanzania (United Republic of) (prices
            normally quoted as integers)
        UAH: Hryvnia Ukraine
        UGX: Uganda Shilling Uganda (prices normally quoted as integers)
        USD: US Dollar United States, American Samoa, Bonaire, Sint
            Eustatius and Saba, British Indian Ocean Territory, Ecuador,
            El Salvador, Guam, Haiti, Marshall Is, Micronesia (Federated
            States of), Northern Mariana Is, Palau, Panama, Puerto Rico,
            Timor-Leste, Turks and Caicos Is, US Minor Outlying Is,
            Virgin Is (British), Virgin Is (US)
        UYU: Peso Uruguayo Uruguay
        UZS: Uzbekistan Sum Uzbekistan (prices normally quoted as
            integers)
        VEB: Bolívar Deprecated, replaced by VEF
        VEF: Bolívar Venezuela (formerly Bolívar fuerte). Deprecated,
            replaced by VES
        VES: Bolívar Soberano Venezuela (replaced VEF from August 2018
            at rate of 100,000:1, and was redenominated by a further
            factor of 1,000,000:1 in late 2021). Only for use in ONIX
            3.0 or later
        VND: Dong Viet Nam (prices normally quoted as integers)
        VUV: Vatu Vanuatu (prices normally quoted as integers)
        WST: Tala Samoa
        XAF: CFA Franc BEAC Cameroon, Central African Republic, Chad,
            Congo, Equatorial Guinea, Gabon (prices normally quoted as
            integers)
        XCD: East Caribbean Dollar Anguilla, Antigua and Barbuda,
            Dominica, Grenada, Montserrat, Saint Kitts and Nevis, Saint
            Lucia, Saint Vincent and the Grenadines
        XCG: Caribbean Guilder Curaçao, Sint Maarten. Only for use in
            ONIX 3.0
        XOF: CFA Franc BCEAO Benin, Burkina Faso, Côte D’Ivoire, Guinea-
            Bissau, Mali, Niger, Senegal, Togo (prices normally quoted
            as integers)
        XPF: CFP Franc French Polynesia, New Caledonia, Wallis and
            Futuna (prices normally quoted as integers)
        YER: Yemeni Rial Yemen (prices normally quoted as integers)
        YUM: Yugoslavian Dinar Deprecated, replaced by CSD
        ZAR: Rand South Africa, Namibia, Lesotho
        ZMK: Kwacha Zambia. Deprecated, replaced with ZMW (prices
            normally quoted as integers)
        ZMW: Zambian Kwacha Zambia
        ZWD: Zimbabwe Dollar Deprecated, replaced with ZWL (prices
            normally quoted as integers)
        ZWG: Zimbabwe Gold Zimbabwe. Also known as ZiG. Only for use in
            ONIX 3.0 or later
        ZWL: Zimbabwe Dollar Deprecated, replaced by ZWG
    """

    AED = "AED"
    AFA = "AFA"
    AFN = "AFN"
    ALL = "ALL"
    AMD = "AMD"
    ANG = "ANG"
    AOA = "AOA"
    ARS = "ARS"
    ATS = "ATS"
    AUD = "AUD"
    AWG = "AWG"
    AZN = "AZN"
    BAM = "BAM"
    BBD = "BBD"
    BDT = "BDT"
    BEF = "BEF"
    BGL = "BGL"
    BGN = "BGN"
    BHD = "BHD"
    BIF = "BIF"
    BMD = "BMD"
    BND = "BND"
    BOB = "BOB"
    BRL = "BRL"
    BSD = "BSD"
    BTN = "BTN"
    BWP = "BWP"
    BYR = "BYR"
    BYN = "BYN"
    BZD = "BZD"
    CAD = "CAD"
    CDF = "CDF"
    CHF = "CHF"
    CLP = "CLP"
    CNY = "CNY"
    COP = "COP"
    CRC = "CRC"
    CSD = "CSD"
    CUC = "CUC"
    CUP = "CUP"
    CVE = "CVE"
    CYP = "CYP"
    CZK = "CZK"
    DEM = "DEM"
    DJF = "DJF"
    DKK = "DKK"
    DOP = "DOP"
    DZD = "DZD"
    EEK = "EEK"
    EGP = "EGP"
    ERN = "ERN"
    ESP = "ESP"
    ETB = "ETB"
    EUR = "EUR"
    FIM = "FIM"
    FJD = "FJD"
    FKP = "FKP"
    FRF = "FRF"
    GBP = "GBP"
    GEL = "GEL"
    GHC = "GHC"
    GHS = "GHS"
    GIP = "GIP"
    GMD = "GMD"
    GNF = "GNF"
    GRD = "GRD"
    GTQ = "GTQ"
    GWP = "GWP"
    GYD = "GYD"
    HKD = "HKD"
    HNL = "HNL"
    HRK = "HRK"
    HTG = "HTG"
    HUF = "HUF"
    IDR = "IDR"
    IEP = "IEP"
    ILS = "ILS"
    INR = "INR"
    IQD = "IQD"
    IRR = "IRR"
    ISK = "ISK"
    ITL = "ITL"
    JMD = "JMD"
    JOD = "JOD"
    JPY = "JPY"
    KES = "KES"
    KGS = "KGS"
    KHR = "KHR"
    KMF = "KMF"
    KPW = "KPW"
    KRW = "KRW"
    KWD = "KWD"
    KYD = "KYD"
    KZT = "KZT"
    LAK = "LAK"
    LBP = "LBP"
    LKR = "LKR"
    LRD = "LRD"
    LSL = "LSL"
    LTL = "LTL"
    LUF = "LUF"
    LVL = "LVL"
    LYD = "LYD"
    MAD = "MAD"
    MDL = "MDL"
    MGA = "MGA"
    MGF = "MGF"
    MKD = "MKD"
    MMK = "MMK"
    MNT = "MNT"
    MOP = "MOP"
    MRO = "MRO"
    MRU = "MRU"
    MTL = "MTL"
    MUR = "MUR"
    MVR = "MVR"
    MWK = "MWK"
    MXN = "MXN"
    MYR = "MYR"
    MZN = "MZN"
    NAD = "NAD"
    NGN = "NGN"
    NIO = "NIO"
    NLG = "NLG"
    NOK = "NOK"
    NPR = "NPR"
    NZD = "NZD"
    OMR = "OMR"
    PAB = "PAB"
    PEN = "PEN"
    PGK = "PGK"
    PHP = "PHP"
    PKR = "PKR"
    PLN = "PLN"
    PTE = "PTE"
    PYG = "PYG"
    QAR = "QAR"
    ROL = "ROL"
    RON = "RON"
    RSD = "RSD"
    RUB = "RUB"
    RUR = "RUR"
    RWF = "RWF"
    SAR = "SAR"
    SBD = "SBD"
    SCR = "SCR"
    SDD = "SDD"
    SDG = "SDG"
    SEK = "SEK"
    SGD = "SGD"
    SHP = "SHP"
    SIT = "SIT"
    SKK = "SKK"
    SLE = "SLE"
    SLL = "SLL"
    SOS = "SOS"
    SRD = "SRD"
    SRG = "SRG"
    STD = "STD"
    STN = "STN"
    SVC = "SVC"
    SYP = "SYP"
    SZL = "SZL"
    THB = "THB"
    TJS = "TJS"
    TMM = "TMM"
    TMT = "TMT"
    TND = "TND"
    TOP = "TOP"
    TPE = "TPE"
    TRL = "TRL"
    TRY = "TRY"
    TTD = "TTD"
    TWD = "TWD"
    TZS = "TZS"
    UAH = "UAH"
    UGX = "UGX"
    USD = "USD"
    UYU = "UYU"
    UZS = "UZS"
    VEB = "VEB"
    VEF = "VEF"
    VES = "VES"
    VND = "VND"
    VUV = "VUV"
    WST = "WST"
    XAF = "XAF"
    XCD = "XCD"
    XCG = "XCG"
    XOF = "XOF"
    XPF = "XPF"
    YER = "YER"
    YUM = "YUM"
    ZAR = "ZAR"
    ZMK = "ZMK"
    ZMW = "ZMW"
    ZWD = "ZWD"
    ZWG = "ZWG"
    ZWL = "ZWL"
