from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List121(Enum):
    """
    Text script – based on ISO 15924.

    Attributes:
        ADLM: Adlam Only for use in ONIX 3.0 or later
        AFAK: Afaka Script is not supported by Unicode
        AGHB: Caucasian Albanian Ancient/historic script. Only for use
            in ONIX 3.0 or later
        AHOM: Ahom, Tai Ahom Ancient/historic script. Only for use in
            ONIX 3.0 or later
        ARAB: Arabic
        ARAN: Arabic (Nastaliq variant) Typographic variant of Arabic.
            Only for use in ONIX 3.0 or later
        ARMI: Imperial Aramaic Ancient/historic script
        ARMN: Armenian
        AVST: Avestan Ancient/historic script
        BALI: Balinese
        BAMU: Bamun
        BASS: Bassa Vah Ancient/historic script
        BATK: Batak
        BENG: Bengali (Bangla)
        BERF: Beria Erfe Only for use in ONIX 3.0 or later
        BHKS: Bhaiksuki Ancient/historic script. Only for use in ONIX
            3.0 or later
        BLIS: Blissymbols Script is not supported by Unicode
        BOPO: Bopomofo
        BRAH: Brahmi Ancient/historic script
        BRAI: Braille
        BUGI: Buginese
        BUHD: Buhid
        CAKM: Chakma
        CANS: Unified Canadian Aboriginal Syllabics
        CARI: Carian Ancient/historic script
        CHAM: Cham
        CHER: Cherokee
        CHIS: Chisoi Script is not supported by Unicode. Only for use in
            ONIX 3.0 or later
        CHRS: Chorasmian Khwārezmian. Ancient/historic script. Only for
            use in ONIX 3.0 or later
        CIRT: Cirth Script is not supported by Unicode
        COPT: Coptic Ancient/historic script
        CPMN: Cypro-Minoan Ancient/historic script. Only for use in ONIX
            3.0 or later
        CPRT: Cypriot Ancient/historic script
        CYRL: Cyrillic
        CYRS: Cyrillic (Old Church Slavonic variant) Ancient/historic,
            typographic variant of Cyrillic
        DEVA: Devanagari (Nagari)
        DIAK: Dives Akuru Ancient/historic script. Only for use in ONIX
            3.0 or later
        DOGR: Dogra Only for use in ONIX 3.0 or later
        DSRT: Deseret (Mormon)
        DUPL: Duployan shorthand, Duployan stenography
        EGYD: Egyptian demotic Script is not supported by Unicode
        EGYH: Egyptian hieratic Script is not supported by Unicode
        EGYP: Egyptian hieroglyphs Ancient/historic script
        ELBA: Elbasan Ancient/historic script
        ELYM: Elymaic Ancient/historic script. Only for use in ONIX 3.0
            or later
        ETHI: Ethiopic (Ge‘ez)
        GARA: Garay Only for use in ONIX 3.0 or later
        GEOK: Khutsuri (Asomtavruli and Khutsuri) Georgian in Unicode
        GEOR: Georgian (Mkhedruli and Mtavruli)
        GLAG: Glagolitic Ancient/historic script
        GONG: Gunjala Gondi Only for use in ONIX 3.0 or later
        GONM: Masaram Gondi Only for use in ONIX 3.0 or later
        GOTH: Gothic Ancient/historic script
        GRAN: Grantha Ancient/historic script
        GREK: Greek
        GUJR: Gujarati
        GUKH: Gurung Khema Only for use in ONIX 3.0 or later
        GURU: Gurmukhi
        HANB: Han with Bopomofo See Hani, Bopo. Only for use in ONIX 3.0
            or later
        HANG: Hangul (Hangŭl, Hangeul)
        HANI: Han (Hanzi, Kanji, Hanja)
        HANO: Hanunoo (Hanunóo)
        HANS: Han (Simplified variant) Subset of Hani
        HANT: Han (Traditional variant) Subset of Hani
        HATR: Hatran Ancient/historic script. Only for use in ONIX 3.0
            or later
        HEBR: Hebrew
        HIRA: Hiragana
        HLUW: Anatolian Hieroglyphs (Luwian Hieroglyphs, Hittite
            Hieroglyphs) Ancient/historic script. Only for use in ONIX
            3.0 or later
        HMNG: Pahawh Hmong
        HMNP: Nyiakeng Puachue Hmong Only for use in ONIX 3.0 or later
        HNTL: Han (Traditional) with Latin (alias for Hant + Latn) See
            Hant, Latn. Only for use in ONIX 3.0 or later
        HRKT: Japanese syllabaries (alias for Hiragana + Katakana) See
            Hira, Kana
        HUNG: Old Hungarian (Hungarian Runic) Ancient/historic script
        INDS: Indus (Harappan) Script is not supported by Unicode
        ITAL: Old Italic (Etruscan, Oscan, etc.) Ancient/historic script
        JAMO: Jamo (alias for Jamo subset of Hangul) Subset of Hang.
            Only for use in ONIX 3.0 or later
        JAVA: Javanese
        JPAN: Japanese (alias for Han + Hiragana + Katakana) See Hani,
            Hira and Kana
        JURC: Jurchen Script is not supported by Unicode
        KALI: Kayah Li
        KANA: Katakana
        KAWI: Kawi Ancient/historic script. Only for use in ONIX 3.0 or
            later
        KHAR: Kharoshthi Ancient/historic script
        KHMR: Khmer
        KHOJ: Khojki Ancient/historic script
        KITL: Khitan large script Script is not supported by Unicode.
            Only for use in ONIX 3.0 or later
        KITS: Khitan small script Only for use in ONIX 3.0 or later
        KNDA: Kannada
        KORE: Korean (alias for Hangul + Han) See Hani and Hang
        KPEL: Kpelle Script is not supported by Unicode
        KRAI: Kirat Rai Only for use in ONIX 3.0 or later
        KTHI: Kaithi Ancient/historic script
        LANA: Tai Tham (Lanna)
        LAOO: Lao
        LATF: Latin (Fraktur variant) Typographic variant of Latin
        LATG: Latin (Gaelic variant) Typographic variant of Latin
        LATN: Latin
        LEKE: Leke Script is not supported by Unicode. Only for use in
            ONIX 3.0 or later
        LEPC: Lepcha (Róng)
        LIMB: Limbu
        LINA: Linear A Ancient/historic script
        LINB: Linear B Ancient/historic script
        LISU: Lisu (Fraser)
        LOMA: Loma Script is not supported by Unicode
        LYCI: Lycian Ancient/historic script
        LYDI: Lydian Ancient/historic script
        MAHJ: Mahajani Ancient/historic script. Only for use in ONIX 3.0
            or later
        MAKA: Makasar Only for use in ONIX 3.0 or later
        MAND: Mandaic, Mandaean
        MANI: Manichaean Ancient/historic script
        MARC: Marchen Ancient/historic script. Only for use in ONIX 3.0
            or later
        MAYA: Mayan hieroglyphs Script is not supported by Unicode
        MEDF: Medefaidrin (Oberi Okaime, Oberi Ɔkaimɛ) Script is not
            supported by Unicode. Only for use in ONIX 3.0 or later
        MEND: Mende Kikakui
        MERC: Meroitic Cursive Ancient/historic script
        MERO: Meroitic Hieroglyphs Ancient/historic script
        MLYM: Malayalam
        MODI: Modi, Moḍī Ancient/historic script. Only for use in ONIX
            3.0 or later
        MONG: Mongolian Includes Clear, Manchu scripts
        MOON: Moon (Moon code, Moon script, Moon type) Script is not
            supported by Unicode
        MROO: Mro, Mru
        MTEI: Meitei Mayek (Meithei, Meetei)
        MULT: Multani Ancient/historic script. Only for use in ONIX 3.0
            or later
        MYMR: Myanmar (Burmese)
        NAGM: Nag Mundari Only for use in ONIX 3.0 or later
        NAND: Nandinagari Ancient/historic script. Only for use in ONIX
            3.0 or later
        NARB: Old North Arabian (Ancient North Arabian) Ancient/historic
            script
        NBAT: Nabatean Ancient/historic script
        NEWA: Newa, Newar, Newari, Nepāla lipi Only for use in ONIX 3.0
            or later
        NKDB: Nakhi Tomba (Naxi Dongba) Script is not supported by
            Unicode. Only for use in ONIX 3.0 or later
        NKGB: Nakhi Geba (’Na-’Khi ²Ggŏ-¹baw, Naxi Geba) Script is not
            supported by Unicode
        NKOO: N’Ko
        NSHU: Nüshu
        OGAM: Ogham Ancient/historic script
        OLCK: Ol Chiki (Ol Cemet’, Ol, Santali)
        ONAO: Ol Onal Only for use in ONIX 3.0 or later
        ORKH: Old Turkic, Orkhon Runic Ancient/historic script
        ORYA: Oriya (Odia)
        OSGE: Osage Only for use in ONIX 3.0 or later
        OSMA: Osmanya
        OUGR: Old Uyghur Ancient/historic script. Only for use in ONIX
            3.0 or later
        PALM: Palmyrene Ancient/historic script
        PAUC: Pau Cin Hau Only for use in ONIX 3.0 or later
        PCUN: Proto-Cuneiform Ancient/historic script, not supported by
            Unicode. Only for use in ONIX 3.0 or later
        PELM: Proto-Elamite Ancient/historic script, not supported by
            Unicode. Only for use in ONIX 3.0 or later
        PERM: Old Permic Ancient/historic script
        PHAG: Phags-pa Ancient/historic script
        PHLI: Inscriptional Pahlavi Ancient/historic script
        PHLP: Psalter Pahlavi Ancient/historic script
        PHLV: Book Pahlavi Script is not supported by Unicode
        PHNX: Phoenician Ancient/historic script
        PIQD: Klingon (KLI plqaD) Script is not supported by Unicode.
            Only for use in ONIX 3.0 or later
        PLRD: Miao (Pollard)
        PRTI: Inscriptional Parthian Ancient/historic script
        PSIN: Proto-Sinaitic Ancient/historic script, not supported by
            Unicode. Only for use in ONIX 3.0 or later
        QAAA: Reserved for private use (start)
        QABP: Picture Communication Symbols (PCS) ONIX local code for
            graphical symbols used in augmentative and alternative
            communication and education, not listed in ISO 15924. Only
            for use in ONIX 3.0 or later
        QABW: Widgit symbols ONIX local code for graphical symbols used
            in augmentative and alternative communication and education,
            not listed in ISO 15924. Only for use in ONIX 3.0 or later
        QABX: Reserved for private use (end)
        RANJ: Ranjana Script is not supported by Unicode. Only for use
            in ONIX 3.0 or later
        RJNG: Rejang (Redjang, Kaganga)
        ROHG: Hanifi Rohingya Only for use in ONIX 3.0 or later
        RORO: Rongorongo Script is not supported by Unicode
        RUNR: Runic Ancient/historic script
        SAMR: Samaritan
        SARA: Sarati Script is not supported by Unicode
        SARB: Old South Arabian Ancient/historic script
        SAUR: Saurashtra
        SEAL: (Small) Seal Script is not supported by Unicode. Only for
            use in ONIX 3.0 or later
        SGNW: SignWriting
        SHAW: Shavian (Shaw)
        SHRD: Sharada, Śāradā
        SHUI: Shuishu Only for use in ONIX 3.0 or later
        SIDD: Siddham, Siddhaṃ, Siddhamātṛkā Ancient/historic script.
            Only for use in ONIX 3.0 or later
        SIDT: Sidetic Only for use in ONIX 3.0 or later
        SIND: Khudawadi, Sindhi
        SINH: Sinhala
        SOGD: Sogdian Ancient/historic script. Only for use in ONIX 3.0
            or later
        SOGO: Old Sogdian Ancient/historic script. Only for use in ONIX
            3.0 or later
        SORA: Sora Sompeng
        SOYO: Soyombo Only for use in ONIX 3.0 or later
        SUND: Sundanese
        SUNU: Sunuwar Only for use in ONIX 3.0 or later
        SYLO: Syloti Nagri
        SYRC: Syriac
        SYRE: Syriac (Estrangelo variant) Typographic variant of Syriac
        SYRJ: Syriac (Western variant) Typographic variant of Syriac
        SYRN: Syriac (Eastern variant) Typographic variant of Syriac
        TAGB: Tagbanwa
        TAKR: Takri, Ṭākrī, Ṭāṅkrī
        TALE: Tai Le
        TALU: New Tai Lue
        TAML: Tamil
        TANG: Tangut Ancient/historic script
        TAVT: Tai Viet
        TAYO: Tai Yo Only for use in ONIX 3.0 or later
        TELU: Telugu
        TENG: Tengwar Script is not supported by Unicode
        TFNG: Tifinagh (Berber)
        TGLG: Tagalog (Baybayin, Alibata)
        THAA: Thaana
        THAI: Thai
        TIBT: Tibetan
        TIRH: Tirhuta
        TNSA: Tangsa Only for use in ONIX 3.0 or later
        TODR: Todhri Only for use in ONIX 3.0 or later
        TOLS: Tolong Siki Only for use in ONIX 3.0 or later
        TOTO: Toto Only for use in ONIX 3.0 or later
        TUTG: Tulu-Tigalari Only for use in ONIX 3.0 or later
        UGAR: Ugaritic Ancient/historic script
        VAII: Vai
        VISP: Visible Speech Script is not supported by Unicode
        VITH: Vithkuqi Ancient/historic script. Only for use in ONIX 3.0
            or later
        WARA: Warang Citi (Varang Kshiti)
        WCHO: Wancho Only for use in ONIX 3.0 or later
        WOLE: Woleai Script is not supported by Unicode
        XPEO: Old Persian Ancient/historic script
        XSUX: Cuneiform, Sumero-Akkadian Ancient/historic script
        YEZI: Yezidi Ancient/historic script. Only for use in ONIX 3.0
            or later
        YIII: Yi
        ZANB: Zanabazar Square (Zanabazarin Dörböljin Useg, Xewtee
            Dörböljin Bicig, Horizontal Square Script) Only for use in
            ONIX 3.0 or later
        ZMTH: Mathematical notation Not a script in Unicode
        ZSYE: Symbols (Emoji variant) Not a script in Unicode. Only for
            use in ONIX 3.0 or later
        ZSYM: Symbols Not a script in Unicode
        ZXXX: Code for unwritten documents Not a script in Unicode
        ZINH: Code for inherited script
        ZYYY: Code for undetermined script
        ZZZZ: Code for uncoded script
    """

    ADLM = "Adlm"
    AFAK = "Afak"
    AGHB = "Aghb"
    AHOM = "Ahom"
    ARAB = "Arab"
    ARAN = "Aran"
    ARMI = "Armi"
    ARMN = "Armn"
    AVST = "Avst"
    BALI = "Bali"
    BAMU = "Bamu"
    BASS = "Bass"
    BATK = "Batk"
    BENG = "Beng"
    BERF = "Berf"
    BHKS = "Bhks"
    BLIS = "Blis"
    BOPO = "Bopo"
    BRAH = "Brah"
    BRAI = "Brai"
    BUGI = "Bugi"
    BUHD = "Buhd"
    CAKM = "Cakm"
    CANS = "Cans"
    CARI = "Cari"
    CHAM = "Cham"
    CHER = "Cher"
    CHIS = "Chis"
    CHRS = "Chrs"
    CIRT = "Cirt"
    COPT = "Copt"
    CPMN = "Cpmn"
    CPRT = "Cprt"
    CYRL = "Cyrl"
    CYRS = "Cyrs"
    DEVA = "Deva"
    DIAK = "Diak"
    DOGR = "Dogr"
    DSRT = "Dsrt"
    DUPL = "Dupl"
    EGYD = "Egyd"
    EGYH = "Egyh"
    EGYP = "Egyp"
    ELBA = "Elba"
    ELYM = "Elym"
    ETHI = "Ethi"
    GARA = "Gara"
    GEOK = "Geok"
    GEOR = "Geor"
    GLAG = "Glag"
    GONG = "Gong"
    GONM = "Gonm"
    GOTH = "Goth"
    GRAN = "Gran"
    GREK = "Grek"
    GUJR = "Gujr"
    GUKH = "Gukh"
    GURU = "Guru"
    HANB = "Hanb"
    HANG = "Hang"
    HANI = "Hani"
    HANO = "Hano"
    HANS = "Hans"
    HANT = "Hant"
    HATR = "Hatr"
    HEBR = "Hebr"
    HIRA = "Hira"
    HLUW = "Hluw"
    HMNG = "Hmng"
    HMNP = "Hmnp"
    HNTL = "Hntl"
    HRKT = "Hrkt"
    HUNG = "Hung"
    INDS = "Inds"
    ITAL = "Ital"
    JAMO = "Jamo"
    JAVA = "Java"
    JPAN = "Jpan"
    JURC = "Jurc"
    KALI = "Kali"
    KANA = "Kana"
    KAWI = "Kawi"
    KHAR = "Khar"
    KHMR = "Khmr"
    KHOJ = "Khoj"
    KITL = "Kitl"
    KITS = "Kits"
    KNDA = "Knda"
    KORE = "Kore"
    KPEL = "Kpel"
    KRAI = "Krai"
    KTHI = "Kthi"
    LANA = "Lana"
    LAOO = "Laoo"
    LATF = "Latf"
    LATG = "Latg"
    LATN = "Latn"
    LEKE = "Leke"
    LEPC = "Lepc"
    LIMB = "Limb"
    LINA = "Lina"
    LINB = "Linb"
    LISU = "Lisu"
    LOMA = "Loma"
    LYCI = "Lyci"
    LYDI = "Lydi"
    MAHJ = "Mahj"
    MAKA = "Maka"
    MAND = "Mand"
    MANI = "Mani"
    MARC = "Marc"
    MAYA = "Maya"
    MEDF = "Medf"
    MEND = "Mend"
    MERC = "Merc"
    MERO = "Mero"
    MLYM = "Mlym"
    MODI = "Modi"
    MONG = "Mong"
    MOON = "Moon"
    MROO = "Mroo"
    MTEI = "Mtei"
    MULT = "Mult"
    MYMR = "Mymr"
    NAGM = "Nagm"
    NAND = "Nand"
    NARB = "Narb"
    NBAT = "Nbat"
    NEWA = "Newa"
    NKDB = "Nkdb"
    NKGB = "Nkgb"
    NKOO = "Nkoo"
    NSHU = "Nshu"
    OGAM = "Ogam"
    OLCK = "Olck"
    ONAO = "Onao"
    ORKH = "Orkh"
    ORYA = "Orya"
    OSGE = "Osge"
    OSMA = "Osma"
    OUGR = "Ougr"
    PALM = "Palm"
    PAUC = "Pauc"
    PCUN = "Pcun"
    PELM = "Pelm"
    PERM = "Perm"
    PHAG = "Phag"
    PHLI = "Phli"
    PHLP = "Phlp"
    PHLV = "Phlv"
    PHNX = "Phnx"
    PIQD = "Piqd"
    PLRD = "Plrd"
    PRTI = "Prti"
    PSIN = "Psin"
    QAAA = "Qaaa"
    QABP = "Qabp"
    QABW = "Qabw"
    QABX = "Qabx"
    RANJ = "Ranj"
    RJNG = "Rjng"
    ROHG = "Rohg"
    RORO = "Roro"
    RUNR = "Runr"
    SAMR = "Samr"
    SARA = "Sara"
    SARB = "Sarb"
    SAUR = "Saur"
    SEAL = "Seal"
    SGNW = "Sgnw"
    SHAW = "Shaw"
    SHRD = "Shrd"
    SHUI = "Shui"
    SIDD = "Sidd"
    SIDT = "Sidt"
    SIND = "Sind"
    SINH = "Sinh"
    SOGD = "Sogd"
    SOGO = "Sogo"
    SORA = "Sora"
    SOYO = "Soyo"
    SUND = "Sund"
    SUNU = "Sunu"
    SYLO = "Sylo"
    SYRC = "Syrc"
    SYRE = "Syre"
    SYRJ = "Syrj"
    SYRN = "Syrn"
    TAGB = "Tagb"
    TAKR = "Takr"
    TALE = "Tale"
    TALU = "Talu"
    TAML = "Taml"
    TANG = "Tang"
    TAVT = "Tavt"
    TAYO = "Tayo"
    TELU = "Telu"
    TENG = "Teng"
    TFNG = "Tfng"
    TGLG = "Tglg"
    THAA = "Thaa"
    THAI = "Thai"
    TIBT = "Tibt"
    TIRH = "Tirh"
    TNSA = "Tnsa"
    TODR = "Todr"
    TOLS = "Tols"
    TOTO = "Toto"
    TUTG = "Tutg"
    UGAR = "Ugar"
    VAII = "Vaii"
    VISP = "Visp"
    VITH = "Vith"
    WARA = "Wara"
    WCHO = "Wcho"
    WOLE = "Wole"
    XPEO = "Xpeo"
    XSUX = "Xsux"
    YEZI = "Yezi"
    YIII = "Yiii"
    ZANB = "Zanb"
    ZMTH = "Zmth"
    ZSYE = "Zsye"
    ZSYM = "Zsym"
    ZXXX = "Zxxx"
    ZINH = "Zinh"
    ZYYY = "Zyyy"
    ZZZZ = "Zzzz"
