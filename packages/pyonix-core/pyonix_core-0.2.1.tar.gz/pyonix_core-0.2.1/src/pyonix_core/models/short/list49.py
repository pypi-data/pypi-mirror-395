from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List49(Enum):
    """
    Region – based on ISO 3166-2.

    Attributes:
        AU_CT: Australian Capital Territory
        AU_NS: New South Wales
        AU_NT: Northern Territory
        AU_QL: Queensland
        AU_SA: South Australia
        AU_TS: Tasmania
        AU_VI: Victoria
        AU_WA: Western Australia
        BE_BRU: Brussels-Capital Region Only for use in ONIX 3.0 or
            later
        BE_VLG: Flemish Region Only for use in ONIX 3.0 or later
        BE_WAL: Walloon Region Only for use in ONIX 3.0 or later
        CA_AB: Alberta
        CA_BC: British Columbia
        CA_MB: Manitoba
        CA_NB: New Brunswick
        CA_NL: Newfoundland and Labrador
        CA_NS: Nova Scotia
        CA_NT: Northwest Territories
        CA_NU: Nunavut
        CA_ON: Ontario
        CA_PE: Prince Edward Island
        CA_QC: Quebec
        CA_SK: Saskatchewan
        CA_YT: Yukon Territory
        CN_BJ: Beijing Municipality Only for use in ONIX 3.0 or later
        CN_TJ: Tianjin Municipality Only for use in ONIX 3.0 or later
        CN_HE: Hebei Province Only for use in ONIX 3.0 or later
        CN_SX: Shanxi Province Only for use in ONIX 3.0 or later
        CN_NM: Nei Mongol Autonomous Region Only for use in ONIX 3.0 or
            later
        CN_LN: Liaoning Province Only for use in ONIX 3.0 or later
        CN_JL: Jilin Province Only for use in ONIX 3.0 or later
        CN_HL: Heilongjiang Province Only for use in ONIX 3.0 or later
        CN_SH: Shanghai Municipality Only for use in ONIX 3.0 or later
        CN_JS: Jiangsu Province Only for use in ONIX 3.0 or later
        CN_ZJ: Zhejiang Province Only for use in ONIX 3.0 or later
        CN_AH: Anhui Province Only for use in ONIX 3.0 or later
        CN_FJ: Fujian Province Only for use in ONIX 3.0 or later
        CN_JX: Jiangxi Province Only for use in ONIX 3.0 or later
        CN_SD: Shandong Province Only for use in ONIX 3.0 or later
        CN_HA: Henan Province Only for use in ONIX 3.0 or later
        CN_HB: Hubei Province Only for use in ONIX 3.0 or later
        CN_HN: Hunan Province Only for use in ONIX 3.0 or later
        CN_GD: Guangdong Province Only for use in ONIX 3.0 or later
        CN_GX: Guangxi Zhuangzu Autonomous Region Only for use in ONIX
            3.0 or later
        CN_HI: Hainan Province Only for use in ONIX 3.0 or later
        CN_CQ: Chongqing Municipality Only for use in ONIX 3.0 or later
        CN_SC: Sichuan Province Only for use in ONIX 3.0 or later
        CN_GZ: Guizhou Province Only for use in ONIX 3.0 or later
        CN_YN: Yunnan Province Only for use in ONIX 3.0 or later
        CN_XZ: Tibet Autonomous Region Only for use in ONIX 3.0 or later
        CN_SN: Shaanxi Province Only for use in ONIX 3.0 or later
        CN_GS: Gansu Province Only for use in ONIX 3.0 or later
        CN_QH: Qinghai Province Only for use in ONIX 3.0 or later
        CN_NX: Ningxia Huizu Autonomous Region Only for use in ONIX 3.0
            or later
        CN_XJ: Xinjiang Uygur Autonomous Region Only for use in ONIX 3.0
            or later
        CN_TW: Taiwan Province Prefer code TW (Taiwan, Province of
            China) from List 91. Only for use in ONIX 3.0 or later
        CN_HK: Hong Kong Special Administrative Region Prefer code HK
            (Hong Kong) from List 91. Only for use in ONIX 3.0 or later
        CN_MO: Macau Special Administrative Region Prefer code MO
            (Macao) from List 91. Only for use in ONIX 3.0 or later
        CN_11: Beijing Municipality Deprecated in favor of CN-BJ
        CN_12: Tianjin Municipality Deprecated in favor of CN-TJ
        CN_13: Hebei Province Deprecated in favor of CN-HE
        CN_14: Shanxi Province Deprecated in favor of CN-SX
        CN_15: Inner Mongolia Autonomous Region Deprecated in favor of
            CN-NM
        CN_21: Liaoning Province Deprecated in favor of CN-LN
        CN_22: Jilin Province Deprecated in favor of CN-JL
        CN_23: Heilongjiang Province Deprecated in favor of CN-HL
        CN_31: Shanghai Municipality Deprecated in favor of CN-SH
        CN_32: Jiangsu Province Deprecated in favor of CN-JS
        CN_33: Zhejiang Province Deprecated in favor of CN-ZJ
        CN_34: Anhui Province Deprecated in favor of CN-AH
        CN_35: Fujian Province Deprecated in favor of CN-FJ
        CN_36: Jiangxi Province Deprecated in favor of CN-JX
        CN_37: Shandong Province Deprecated in favor of CN-SD
        CN_41: Henan Province Deprecated in favor of CN-HA
        CN_42: Hubei Province Deprecated in favor of CN-HB
        CN_43: Hunan Province Deprecated in favor of CN-HN
        CN_44: Guangdong Province Deprecated in favor of CN-GD
        CN_45: Guangxi Zhuang Autonomous Region Deprecated in favor of
            CN-GX
        CN_46: Hainan Province Deprecated in favor of CN-HI
        CN_50: Chongqing Municipality Deprecated in favor of CN-CQ
        CN_51: Sichuan Province Deprecated in favor of CN-SC
        CN_52: Guizhou Province Deprecated in favor of CN-GZ
        CN_53: Yunnan Province Deprecated in favor of CN-YN
        CN_54: Tibet Autonomous Region Deprecated in favor of CN-XZ
        CN_61: Shaanxi Province Deprecated in favor of CN-SN
        CN_62: Gansu Province Deprecated in favor of CN-GS
        CN_63: Qinghai Province Deprecated in favor of CN-QH
        CN_64: Ningxia Hui Autonomous Region Deprecated in favor of CN-
            NX
        CN_65: Xinjiang Uyghur Autonomous Region Deprecated in favor of
            CN-XJ
        CN_71: Taiwan Province Deprecated in favor of CN-TW, but prefer
            code TW (Taiwan, Province of China) from List 91
        CN_91: Hong Kong Special Administrative Region Deprecated in
            favor of CN-HK, but prefer code HK (Hong Kong) from List 91
        CN_92: Macau Special Administrative Region Deprecated in favor
            of CN-MO, but prefer code MO (Macao) from List 91
        ES_CN: Canary Islands
        FR_H: Corsica
        GB_AIR: UK airside Airside outlets at UK international airports
            only
        GB_APS: UK airports All UK airports, including both airside and
            other outlets
        GB_CHA: Channel Islands Deprecated, replaced by country codes GG
            – Guernsey, and JE – Jersey from List 91
        GB_ENG: England
        GB_EWS: England, Wales, Scotland UK excluding Northern Ireland.
            Deprecated – use separate region codes GB-ENG, GB-SCT, GB-
            WLS instead
        GB_IOM: Isle of Man Deprecated, replaced by country code IM –
            Isle of Man from List 91
        GB_NIR: Northern Ireland
        GB_SCT: Scotland
        GB_WLS: Wales
        IE_AIR: Ireland airside Airside outlets at Irish international
            airports only
        IT_AG: Agrigento
        IT_AL: Alessandria
        IT_AN: Ancona
        IT_AO: Aosta
        IT_AR: Arezzo
        IT_AP: Ascoli Piceno
        IT_AT: Asti
        IT_AV: Avellino
        IT_BA: Bari
        IT_BT: Barletta-Andria-Trani
        IT_BL: Belluno
        IT_BN: Benevento
        IT_BG: Bergamo
        IT_BI: Biella
        IT_BO: Bologna
        IT_BZ: Bolzano
        IT_BS: Brescia
        IT_BR: Brindisi
        IT_CA: Cagliari
        IT_CL: Caltanissetta
        IT_CB: Campobasso
        IT_CI: Carbonia-Iglesias
        IT_CE: Caserta
        IT_CT: Catania
        IT_CZ: Catanzaro
        IT_CH: Chieti
        IT_CO: Como
        IT_CS: Cosenza
        IT_CR: Cremona
        IT_KR: Crotone
        IT_CN: Cuneo
        IT_EN: Enna
        IT_FM: Fermo
        IT_FE: Ferrara
        IT_FI: Firenze
        IT_FG: Foggia
        IT_FC: Forlì-Cesena
        IT_FR: Frosinone
        IT_GE: Genova
        IT_GO: Gorizia
        IT_GR: Grosseto
        IT_IM: Imperia
        IT_IS: Isernia
        IT_SP: La Spezia
        IT_AQ: L’Aquila
        IT_LT: Latina
        IT_LE: Lecce
        IT_LC: Lecco
        IT_LI: Livorno
        IT_LO: Lodi
        IT_LU: Lucca
        IT_MC: Macerata
        IT_MN: Mantova
        IT_MS: Massa-Carrara
        IT_MT: Matera
        IT_VS: Medio Campidano
        IT_ME: Messina
        IT_MI: Milano
        IT_MO: Modena
        IT_MB: Monza e Brianza
        IT_NA: Napoli
        IT_NO: Novara
        IT_NU: Nuoro
        IT_OG: Ogliastra
        IT_OT: Olbia-Tempio
        IT_OR: Oristano
        IT_PD: Padova
        IT_PA: Palermo
        IT_PR: Parma
        IT_PV: Pavia
        IT_PG: Perugia
        IT_PU: Pesaro e Urbino
        IT_PE: Pescara
        IT_PC: Piacenza
        IT_PI: Pisa
        IT_PT: Pistoia
        IT_PN: Pordenone
        IT_PZ: Potenza
        IT_PO: Prato
        IT_RG: Ragusa
        IT_RA: Ravenna
        IT_RC: Reggio Calabria
        IT_RE: Reggio Emilia
        IT_RI: Rieti
        IT_RN: Rimini
        IT_RM: Roma
        IT_RO: Rovigo
        IT_SA: Salerno
        IT_SS: Sassari
        IT_SV: Savona
        IT_SI: Siena
        IT_SR: Siracusa
        IT_SO: Sondrio
        IT_TA: Taranto
        IT_TE: Teramo
        IT_TR: Terni
        IT_TO: Torino
        IT_TP: Trapani
        IT_TN: Trento
        IT_TV: Treviso
        IT_TS: Trieste
        IT_UD: Udine
        IT_VA: Varese
        IT_VE: Venezia
        IT_VB: Verbano-Cusio-Ossola
        IT_VC: Vercelli
        IT_VR: Verona
        IT_VV: Vibo Valentia
        IT_VI: Vicenza
        IT_VT: Viterbo
        RS_KM: Kosovo-Metohija
        RS_VO: Vojvodina
        RU_AD: Republic of Adygeya
        RU_AL: Republic of Altay
        RU_BA: Republic of Bashkortostan
        RU_BU: Republic of Buryatiya
        RU_CE: Chechenskaya Republic
        RU_CU: Chuvashskaya Republic
        RU_DA: Republic of Dagestan
        RU_IN: Republic of Ingushetiya
        RU_KB: Kabardino-Balkarskaya Republic
        RU_KL: Republic of Kalmykiya
        RU_KC: Karachayevo-Cherkesskaya Republic
        RU_KR: Republic of Kareliya
        RU_KK: Republic of Khakasiya
        RU_KO: Republic of Komi
        RU_ME: Republic of Mariy El
        RU_MO: Republic of Mordoviya
        RU_SA: Republic of Sakha (Yakutiya)
        RU_SE: Republic of Severnaya Osetiya-Alaniya
        RU_TA: Republic of Tatarstan
        RU_TY: Republic of Tyva (Tuva)
        RU_UD: Udmurtskaya Republic
        RU_ALT: Altayskiy Administrative Territory
        RU_KAM: Kamchatskiy Administrative Territory
        RU_KHA: Khabarovskiy Administrative Territory
        RU_KDA: Krasnodarskiy Administrative Territory
        RU_KYA: Krasnoyarskiy Administrative Territory
        RU_PER: Permskiy Administrative Territory
        RU_PRI: Primorskiy Administrative Territory
        RU_STA: Stavropol’skiy Administrative Territory
        RU_ZAB: Zabaykal’skiy Administrative Territory
        RU_AMU: Amurskaya Administrative Region
        RU_ARK: Arkhangel’skaya Administrative Region
        RU_AST: Astrakhanskaya Administrative Region
        RU_BEL: Belgorodskaya Administrative Region
        RU_BRY: Bryanskaya Administrative Region
        RU_CHE: Chelyabinskaya Administrative Region
        RU_IRK: Irkutskaya Administrative Region
        RU_IVA: Ivanovskaya Administrative Region
        RU_KGD: Kaliningradskaya Administrative Region
        RU_KLU: Kaluzhskaya Administrative Region
        RU_KEM: Kemerovskaya Administrative Region
        RU_KIR: Kirovskaya Administrative Region
        RU_KOS: Kostromskaya Administrative Region
        RU_KGN: Kurganskaya Administrative Region
        RU_KRS: Kurskaya Administrative Region
        RU_LEN: Leningradskaya Administrative Region
        RU_LIP: Lipetskaya Administrative Region
        RU_MAG: Magadanskaya Administrative Region
        RU_MOS: Moskovskaya Administrative Region
        RU_MUR: Murmanskaya Administrative Region
        RU_NIZ: Nizhegorodskaya Administrative Region
        RU_NGR: Novgorodskaya Administrative Region
        RU_NVS: Novosibirskaya Administrative Region
        RU_OMS: Omskaya Administrative Region
        RU_ORE: Orenburgskaya Administrative Region
        RU_ORL: Orlovskaya Administrative Region
        RU_PNZ: Penzenskaya Administrative Region
        RU_PSK: Pskovskaya Administrative Region
        RU_ROS: Rostovskaya Administrative Region
        RU_RYA: Ryazanskaya Administrative Region
        RU_SAK: Sakhalinskaya Administrative Region
        RU_SAM: Samarskaya Administrative Region
        RU_SAR: Saratovskaya Administrative Region
        RU_SMO: Smolenskaya Administrative Region
        RU_SVE: Sverdlovskaya Administrative Region
        RU_TAM: Tambovskaya Administrative Region
        RU_TOM: Tomskaya Administrative Region
        RU_TUL: Tul’skaya Administrative Region
        RU_TVE: Tverskaya Administrative Region
        RU_TYU: Tyumenskaya Administrative Region
        RU_ULY: Ul’yanovskaya Administrative Region
        RU_VLA: Vladimirskaya Administrative Region
        RU_VGG: Volgogradskaya Administrative Region
        RU_VLG: Vologodskaya Administrative Region
        RU_VOR: Voronezhskaya Administrative Region
        RU_YAR: Yaroslavskaya Administrative Region
        RU_MOW: Moskva City
        RU_SPE: Sankt-Peterburg City
        RU_YEV: Yevreyskaya Autonomous Administrative Region
        RU_CHU: Chukotskiy Autonomous District
        RU_KHM: Khanty-Mansiyskiy Autonomous District
        RU_NEN: Nenetskiy Autonomous District
        RU_YAN: Yamalo-Nenetskiy Autonomous District
        US_AK: Alaska
        US_AL: Alabama
        US_AR: Arkansas
        US_AZ: Arizona
        US_CA: California
        US_CO: Colorado
        US_CT: Connecticut
        US_DC: District of Columbia
        US_DE: Delaware
        US_FL: Florida
        US_GA: Georgia
        US_HI: Hawaii
        US_IA: Iowa
        US_ID: Idaho
        US_IL: Illinois
        US_IN: Indiana
        US_KS: Kansas
        US_KY: Kentucky
        US_LA: Louisiana
        US_MA: Massachusetts
        US_MD: Maryland
        US_ME: Maine
        US_MI: Michigan
        US_MN: Minnesota
        US_MO: Missouri
        US_MS: Mississippi
        US_MT: Montana
        US_NC: North Carolina
        US_ND: North Dakota
        US_NE: Nebraska
        US_NH: New Hampshire
        US_NJ: New Jersey
        US_NM: New Mexico
        US_NV: Nevada
        US_NY: New York
        US_OH: Ohio
        US_OK: Oklahoma
        US_OR: Oregon
        US_PA: Pennsylvania
        US_RI: Rhode Island
        US_SC: South Carolina
        US_SD: South Dakota
        US_TN: Tennessee
        US_TX: Texas
        US_UT: Utah
        US_VA: Virginia
        US_VT: Vermont
        US_WA: Washington
        US_WI: Wisconsin
        US_WV: West Virginia
        US_WY: Wyoming
        ECZ: Eurozone Countries geographically within continental Europe
            which use the Euro as their sole currency. At the time of
            writing, this is a synonym for ‘AT BE CY EE FI FR DE ES GR
            HR IE IT LT LU LV MT NL PT SI SK’ (the official Eurozone
            20), plus ‘AD MC SM VA ME’ and Kosovo (other Euro-using
            countries in continental Europe). Note some other
            territories using the Euro, but outside continental Europe
            are excluded from this list, and may need to be specified
            separately. ONLY valid in ONIX 3.0, and ONLY within P.26 –
            and this use is itself Deprecated. Use of an explicit list
            of countries instead of ECZ is strongly encouraged
        WORLD: World In ONIX 3.0 and later, may ONLY be used in
            &lt;RegionsIncluded&gt;
    """

    AU_CT = "AU-CT"
    AU_NS = "AU-NS"
    AU_NT = "AU-NT"
    AU_QL = "AU-QL"
    AU_SA = "AU-SA"
    AU_TS = "AU-TS"
    AU_VI = "AU-VI"
    AU_WA = "AU-WA"
    BE_BRU = "BE-BRU"
    BE_VLG = "BE-VLG"
    BE_WAL = "BE-WAL"
    CA_AB = "CA-AB"
    CA_BC = "CA-BC"
    CA_MB = "CA-MB"
    CA_NB = "CA-NB"
    CA_NL = "CA-NL"
    CA_NS = "CA-NS"
    CA_NT = "CA-NT"
    CA_NU = "CA-NU"
    CA_ON = "CA-ON"
    CA_PE = "CA-PE"
    CA_QC = "CA-QC"
    CA_SK = "CA-SK"
    CA_YT = "CA-YT"
    CN_BJ = "CN-BJ"
    CN_TJ = "CN-TJ"
    CN_HE = "CN-HE"
    CN_SX = "CN-SX"
    CN_NM = "CN-NM"
    CN_LN = "CN-LN"
    CN_JL = "CN-JL"
    CN_HL = "CN-HL"
    CN_SH = "CN-SH"
    CN_JS = "CN-JS"
    CN_ZJ = "CN-ZJ"
    CN_AH = "CN-AH"
    CN_FJ = "CN-FJ"
    CN_JX = "CN-JX"
    CN_SD = "CN-SD"
    CN_HA = "CN-HA"
    CN_HB = "CN-HB"
    CN_HN = "CN-HN"
    CN_GD = "CN-GD"
    CN_GX = "CN-GX"
    CN_HI = "CN-HI"
    CN_CQ = "CN-CQ"
    CN_SC = "CN-SC"
    CN_GZ = "CN-GZ"
    CN_YN = "CN-YN"
    CN_XZ = "CN-XZ"
    CN_SN = "CN-SN"
    CN_GS = "CN-GS"
    CN_QH = "CN-QH"
    CN_NX = "CN-NX"
    CN_XJ = "CN-XJ"
    CN_TW = "CN-TW"
    CN_HK = "CN-HK"
    CN_MO = "CN-MO"
    CN_11 = "CN-11"
    CN_12 = "CN-12"
    CN_13 = "CN-13"
    CN_14 = "CN-14"
    CN_15 = "CN-15"
    CN_21 = "CN-21"
    CN_22 = "CN-22"
    CN_23 = "CN-23"
    CN_31 = "CN-31"
    CN_32 = "CN-32"
    CN_33 = "CN-33"
    CN_34 = "CN-34"
    CN_35 = "CN-35"
    CN_36 = "CN-36"
    CN_37 = "CN-37"
    CN_41 = "CN-41"
    CN_42 = "CN-42"
    CN_43 = "CN-43"
    CN_44 = "CN-44"
    CN_45 = "CN-45"
    CN_46 = "CN-46"
    CN_50 = "CN-50"
    CN_51 = "CN-51"
    CN_52 = "CN-52"
    CN_53 = "CN-53"
    CN_54 = "CN-54"
    CN_61 = "CN-61"
    CN_62 = "CN-62"
    CN_63 = "CN-63"
    CN_64 = "CN-64"
    CN_65 = "CN-65"
    CN_71 = "CN-71"
    CN_91 = "CN-91"
    CN_92 = "CN-92"
    ES_CN = "ES-CN"
    FR_H = "FR-H"
    GB_AIR = "GB-AIR"
    GB_APS = "GB-APS"
    GB_CHA = "GB-CHA"
    GB_ENG = "GB-ENG"
    GB_EWS = "GB-EWS"
    GB_IOM = "GB-IOM"
    GB_NIR = "GB-NIR"
    GB_SCT = "GB-SCT"
    GB_WLS = "GB-WLS"
    IE_AIR = "IE-AIR"
    IT_AG = "IT-AG"
    IT_AL = "IT-AL"
    IT_AN = "IT-AN"
    IT_AO = "IT-AO"
    IT_AR = "IT-AR"
    IT_AP = "IT-AP"
    IT_AT = "IT-AT"
    IT_AV = "IT-AV"
    IT_BA = "IT-BA"
    IT_BT = "IT-BT"
    IT_BL = "IT-BL"
    IT_BN = "IT-BN"
    IT_BG = "IT-BG"
    IT_BI = "IT-BI"
    IT_BO = "IT-BO"
    IT_BZ = "IT-BZ"
    IT_BS = "IT-BS"
    IT_BR = "IT-BR"
    IT_CA = "IT-CA"
    IT_CL = "IT-CL"
    IT_CB = "IT-CB"
    IT_CI = "IT-CI"
    IT_CE = "IT-CE"
    IT_CT = "IT-CT"
    IT_CZ = "IT-CZ"
    IT_CH = "IT-CH"
    IT_CO = "IT-CO"
    IT_CS = "IT-CS"
    IT_CR = "IT-CR"
    IT_KR = "IT-KR"
    IT_CN = "IT-CN"
    IT_EN = "IT-EN"
    IT_FM = "IT-FM"
    IT_FE = "IT-FE"
    IT_FI = "IT-FI"
    IT_FG = "IT-FG"
    IT_FC = "IT-FC"
    IT_FR = "IT-FR"
    IT_GE = "IT-GE"
    IT_GO = "IT-GO"
    IT_GR = "IT-GR"
    IT_IM = "IT-IM"
    IT_IS = "IT-IS"
    IT_SP = "IT-SP"
    IT_AQ = "IT-AQ"
    IT_LT = "IT-LT"
    IT_LE = "IT-LE"
    IT_LC = "IT-LC"
    IT_LI = "IT-LI"
    IT_LO = "IT-LO"
    IT_LU = "IT-LU"
    IT_MC = "IT-MC"
    IT_MN = "IT-MN"
    IT_MS = "IT-MS"
    IT_MT = "IT-MT"
    IT_VS = "IT-VS"
    IT_ME = "IT-ME"
    IT_MI = "IT-MI"
    IT_MO = "IT-MO"
    IT_MB = "IT-MB"
    IT_NA = "IT-NA"
    IT_NO = "IT-NO"
    IT_NU = "IT-NU"
    IT_OG = "IT-OG"
    IT_OT = "IT-OT"
    IT_OR = "IT-OR"
    IT_PD = "IT-PD"
    IT_PA = "IT-PA"
    IT_PR = "IT-PR"
    IT_PV = "IT-PV"
    IT_PG = "IT-PG"
    IT_PU = "IT-PU"
    IT_PE = "IT-PE"
    IT_PC = "IT-PC"
    IT_PI = "IT-PI"
    IT_PT = "IT-PT"
    IT_PN = "IT-PN"
    IT_PZ = "IT-PZ"
    IT_PO = "IT-PO"
    IT_RG = "IT-RG"
    IT_RA = "IT-RA"
    IT_RC = "IT-RC"
    IT_RE = "IT-RE"
    IT_RI = "IT-RI"
    IT_RN = "IT-RN"
    IT_RM = "IT-RM"
    IT_RO = "IT-RO"
    IT_SA = "IT-SA"
    IT_SS = "IT-SS"
    IT_SV = "IT-SV"
    IT_SI = "IT-SI"
    IT_SR = "IT-SR"
    IT_SO = "IT-SO"
    IT_TA = "IT-TA"
    IT_TE = "IT-TE"
    IT_TR = "IT-TR"
    IT_TO = "IT-TO"
    IT_TP = "IT-TP"
    IT_TN = "IT-TN"
    IT_TV = "IT-TV"
    IT_TS = "IT-TS"
    IT_UD = "IT-UD"
    IT_VA = "IT-VA"
    IT_VE = "IT-VE"
    IT_VB = "IT-VB"
    IT_VC = "IT-VC"
    IT_VR = "IT-VR"
    IT_VV = "IT-VV"
    IT_VI = "IT-VI"
    IT_VT = "IT-VT"
    RS_KM = "RS-KM"
    RS_VO = "RS-VO"
    RU_AD = "RU-AD"
    RU_AL = "RU-AL"
    RU_BA = "RU-BA"
    RU_BU = "RU-BU"
    RU_CE = "RU-CE"
    RU_CU = "RU-CU"
    RU_DA = "RU-DA"
    RU_IN = "RU-IN"
    RU_KB = "RU-KB"
    RU_KL = "RU-KL"
    RU_KC = "RU-KC"
    RU_KR = "RU-KR"
    RU_KK = "RU-KK"
    RU_KO = "RU-KO"
    RU_ME = "RU-ME"
    RU_MO = "RU-MO"
    RU_SA = "RU-SA"
    RU_SE = "RU-SE"
    RU_TA = "RU-TA"
    RU_TY = "RU-TY"
    RU_UD = "RU-UD"
    RU_ALT = "RU-ALT"
    RU_KAM = "RU-KAM"
    RU_KHA = "RU-KHA"
    RU_KDA = "RU-KDA"
    RU_KYA = "RU-KYA"
    RU_PER = "RU-PER"
    RU_PRI = "RU-PRI"
    RU_STA = "RU-STA"
    RU_ZAB = "RU-ZAB"
    RU_AMU = "RU-AMU"
    RU_ARK = "RU-ARK"
    RU_AST = "RU-AST"
    RU_BEL = "RU-BEL"
    RU_BRY = "RU-BRY"
    RU_CHE = "RU-CHE"
    RU_IRK = "RU-IRK"
    RU_IVA = "RU-IVA"
    RU_KGD = "RU-KGD"
    RU_KLU = "RU-KLU"
    RU_KEM = "RU-KEM"
    RU_KIR = "RU-KIR"
    RU_KOS = "RU-KOS"
    RU_KGN = "RU-KGN"
    RU_KRS = "RU-KRS"
    RU_LEN = "RU-LEN"
    RU_LIP = "RU-LIP"
    RU_MAG = "RU-MAG"
    RU_MOS = "RU-MOS"
    RU_MUR = "RU-MUR"
    RU_NIZ = "RU-NIZ"
    RU_NGR = "RU-NGR"
    RU_NVS = "RU-NVS"
    RU_OMS = "RU-OMS"
    RU_ORE = "RU-ORE"
    RU_ORL = "RU-ORL"
    RU_PNZ = "RU-PNZ"
    RU_PSK = "RU-PSK"
    RU_ROS = "RU-ROS"
    RU_RYA = "RU-RYA"
    RU_SAK = "RU-SAK"
    RU_SAM = "RU-SAM"
    RU_SAR = "RU-SAR"
    RU_SMO = "RU-SMO"
    RU_SVE = "RU-SVE"
    RU_TAM = "RU-TAM"
    RU_TOM = "RU-TOM"
    RU_TUL = "RU-TUL"
    RU_TVE = "RU-TVE"
    RU_TYU = "RU-TYU"
    RU_ULY = "RU-ULY"
    RU_VLA = "RU-VLA"
    RU_VGG = "RU-VGG"
    RU_VLG = "RU-VLG"
    RU_VOR = "RU-VOR"
    RU_YAR = "RU-YAR"
    RU_MOW = "RU-MOW"
    RU_SPE = "RU-SPE"
    RU_YEV = "RU-YEV"
    RU_CHU = "RU-CHU"
    RU_KHM = "RU-KHM"
    RU_NEN = "RU-NEN"
    RU_YAN = "RU-YAN"
    US_AK = "US-AK"
    US_AL = "US-AL"
    US_AR = "US-AR"
    US_AZ = "US-AZ"
    US_CA = "US-CA"
    US_CO = "US-CO"
    US_CT = "US-CT"
    US_DC = "US-DC"
    US_DE = "US-DE"
    US_FL = "US-FL"
    US_GA = "US-GA"
    US_HI = "US-HI"
    US_IA = "US-IA"
    US_ID = "US-ID"
    US_IL = "US-IL"
    US_IN = "US-IN"
    US_KS = "US-KS"
    US_KY = "US-KY"
    US_LA = "US-LA"
    US_MA = "US-MA"
    US_MD = "US-MD"
    US_ME = "US-ME"
    US_MI = "US-MI"
    US_MN = "US-MN"
    US_MO = "US-MO"
    US_MS = "US-MS"
    US_MT = "US-MT"
    US_NC = "US-NC"
    US_ND = "US-ND"
    US_NE = "US-NE"
    US_NH = "US-NH"
    US_NJ = "US-NJ"
    US_NM = "US-NM"
    US_NV = "US-NV"
    US_NY = "US-NY"
    US_OH = "US-OH"
    US_OK = "US-OK"
    US_OR = "US-OR"
    US_PA = "US-PA"
    US_RI = "US-RI"
    US_SC = "US-SC"
    US_SD = "US-SD"
    US_TN = "US-TN"
    US_TX = "US-TX"
    US_UT = "US-UT"
    US_VA = "US-VA"
    US_VT = "US-VT"
    US_WA = "US-WA"
    US_WI = "US-WI"
    US_WV = "US-WV"
    US_WY = "US-WY"
    ECZ = "ECZ"
    WORLD = "WORLD"
