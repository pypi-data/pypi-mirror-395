from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LocaleIDs(Enum):
    """
    Enum class representing locale IDs.
    """
    # Represents a scenario where the language has not been set or specified.
    LanguageNotSet = 0
    # Represents a placeholder or absence of a specific value
    x_none = 127
    # Represents the Afrikaans language as spoken in South Africa.
    af_ZA = 1072
    # Represents the Albanian language (sq) as spoken in Albania (AL).
    sq_AL = 1052
    # Represents the Amharic language used in Ethiopia.
    am_ET = 1118
    # Represents the Swiss German as used in France.
    gsw_FR = 1156
    # Represents the Arabic language as spoken in Algeria.
    ar_DZ = 5121
    # Arabic (Bahrain).
    ar_BH = 15361
    # Represents the Arabic language as spoken in Egypt.
    ar_EG = 3073
    # Represents the Arabic language (ar) as spoken in Iraq (IQ).
    ar_IQ = 2049
    # Represents the Arabic language as spoken in Jordan.
    ar_JO = 11265
    # Represents the Arabic language as used in Kuwait (ar_KW).
    ar_KW = 13313
    # Represents the locale for Lebanese Arabic (ar-LB).
    ar_LB = 12289
    # Represents the Arabic language as spoken in Libya.
    ar_LY = 4097
    # Arabic (Morocco).
    ar_MA = 6145
    # Represents the Arabic language (ar) as spoken in Oman (OM).
    ar_OM = 8193
    # Represents the Arabic language (ar) as used in Qatar (QA).
    ar_QA = 16385
    # Represents the Arabic language (ar) as spoken in Saudi Arabia (SA).
    ar_SA = 1025
    # Arabic (Syria).
    ar_SY = 10241
    # Represents the Arabic language as spoken in Tunisia.
    ar_TN = 7169
    # Represents the Arabic language as spoken in the United Arab Emirates.
    ar_AE = 14337
    # Represents the Arabic language as spoken in Yemen (ar-YE).
    ar_YE = 9217
    # Represents the Armenian language as spoken in Armenia.
    hy_AM = 1067
    # Assamese (India)
    as_IN = 1101
    # Represents the Azerbaijani language using Cyrillic script as spoken in Azerbaijan.
    az_Cyrl_AZ = 2092
    # Represents the Azerbaijani language using the Latin alphabet specifically for Azerbaijan.
    az_Latn_AZ = 1068
    # Bashkir (Russia).
    ba_RU = 1133
    # Basque (Spain).
    eu_ES = 1069
    # Belarusian language (Belarus)
    be_BY = 1059
    # Bengali in Bangladesh.
    bn_BD = 2117
    # Represents the locale for Indian National (Bengali) language.
    bn_IN = 1093
    # Represents the Bosnian language using Cyrillic script as used in Bosnia and Herzegovina.
    bs_Cyrl_BA = 8218
    # Represents the Bosnian language using the Latin script as spoken in Bosnia and Herzegovina.
    bs_Latn_BA = 5146
    # Bulgarian language (Bulgaria).
    bg_BG = 1026
    # Breton in France
    br_FR = 1150
    # Burmese Myanmar
    my_MM = 1109
    # Catalan in Spain
    ca_ES = 1027
    # Cherokee in USA
    chr_US = 1116
    # Chinese(Hong Kong)
    zh_HK = 3076
    # Chinese(Macau)
    zh_MO = 5124
    # Chinese(Simplified)
    zh_CN = 2052
    # Chinese(Singapore)
    zh_SG = 4100
    # Chinese(Taiwan)
    zh_TW = 1028
    # Corsican in France.
    co_FR = 1155
    # Croatian used in Bosnia and Herzegovina.
    hr_BA = 4122
    # Croatian
    hr_HR = 1050
    # Czech
    cs_CZ = 1029
    # Represents Danish (Denmark).
    da_DK = 1030
    # Dari Persian in Afghanistan
    prs_AF = 1164
    # Dhivehi in Maldives
    dv_MV = 1125
    # Represents the locale for Dutch (Flemish) as spoken in Belgium.
    nl_BE = 2067
    # Represents the Dutch language as spoken in the Netherlands.
    nl_NL = 1043
    # Bini in Nigeria
    bin_NG = 1126
    # Represents the locale for Estonian (Estonia).
    et_EE = 1061
    # Represents the locale for English (Australia).
    en_AU = 3081
    # Represents the English language as used in Belize (en-BZ).
    en_BZ = 10249
    # Canadian English
    en_CA = 4105
    # Caribbean English
    en_029 = 9225
    # Represents the English language as used in Hong Kong.
    en_HK = 15369
    # Represents the locale for English as used in India.
    en_IN = 16393
    # English in Indonesia
    en_ID = 14345
    # Represents the locale for English (Ireland).
    en_IE = 6153
    # Represents the English language as spoken in Jamaica.
    en_JM = 8201
    # Malaysian English
    en_MY = 17417
    # Represents the New Zealand English.
    en_NZ = 5129
    # Represents the Filipino language (Filipino) as spoken in the Philippines.
    en_PH = 13321
    # Represents the English language as used in Singapore.
    en_SG = 18441
    # Represents the locale for English (South Africa).
    en_ZA = 7177
    # Represents the English language as spoken in Trinidad and Tobago.
    en_TT = 11273
    # Represents the locale for English as used in the United Kingdom.
    en_GB = 2057
    # English (United States).
    en_US = 1033
    # Represents the locale for Zimbabwe using English as the language.
    en_ZW = 12297
    # Represents the Faroese language (fo) as used in Faroe Islands (FO).
    fo_FO = 1080
    # Philippines
    fil_PH = 1124
    # Represents the Finnish language (Finland).
    fi_FI = 1035
    # Represents the locale for French (Belgium).
    fr_BE = 2060
    # Represents the locale for French (France) as used in Cameroon.
    fr_CM = 11276
    # Represents the Canadian French language.
    fr_CA = 3084
    # French (France) in Democratic Republic of Congo.
    fr_CD = 9228
    # Ivoiran French
    fr_CI = 12300
    # French
    fr_FR = 1036
    # Haitian French
    fr_HT = 15372
    # Luxembourgish French.
    fr_LU = 5132
    # Malian French
    fr_ML = 13324
    # French (Monaco)
    fr_MC = 6156
    # Moroccan French
    fr_MA = 14348
    # Réunion French
    fr_RE = 8204
    # Represents the French language as spoken in Senegal (fr_SN).
    fr_SN = 10252
    # Swiss French.
    fr_CH = 4108
    # French in West Indies
    fr_fr_WINDIES = 7180
    # Represents the language code for Dutch (Netherlands).
    fy_NL = 1122
    # Represents the language code for Filipino (Philippines).
    ff_NG = 1127
    # Scottish Gaelic(United Kingdom)
    gd_GB = 1084
    # Galician in Spain.
    gl_ES = 1110
    # Represents the Georgian language (ka) as used in Georgia (GE).
    ka_GE = 1079
    # Austrian German
    de_AT = 3079
    # German
    de_DE = 1031
    # Liechtenstein German
    de_LI = 5127
    # Luxembourgish German.
    de_LU = 4103
    # Swiss German
    de_CH = 2055
    # Greek
    el_GR = 1032
    # Represents the locale for Guarani (Paraguay).
    gn_PY = 1140
    # Gujarati in India.
    gu_IN = 1095
    # Kalaallisut in Greenland
    kl_GL = 1135
    # Represents the locale for Hausa language using Latin script as spoken in Nigeria.
    ha_Latn_NG = 1128
    # Hawaiian the United States
    haw_US = 1141
    # Hebrew in Israel
    he_IL = 1037
    # Hindi (India).
    hi_IN = 1081
    # Hungarian (Hungary).
    hu_HU = 1038
    # Igbo in Nigeria
    ibb_NG = 1129
    # Icelandic
    is_IS = 1039
    # Represents the Nigerian locale specifically for Nigeria using the Igbo language.
    ig_NG = 1136
    # Indonesian (Bahasa Indonesia).
    id_ID = 1057
    # Inuktitut following the Latin alphabet writing system is used in Canada.
    iu_Latn_CA = 2141
    # Inuktitut used in Canada is written in Inuktitut syllabics.
    iu_Cans_CA = 1117
    # Italian
    it_IT = 1040
    # Swiss Italian
    it_CH = 2064
    # Represents the locale for Irish (Gaelic) as spoken in Ireland.
    ga_IE = 2108
    # Represents the locale for Xhosa language spoken in South Africa.
    xh_ZA = 1076
    # Represents the locale for Afrikaans (South Africa).
    zu_ZA = 1077
    # Kannada in Indian.
    kn_IN = 1099
    # Kanuri in Nigeria
    kr_NG = 1137
    # Kashmiri written by Devanagari script
    ks_Deva = 2144
    # Kashmiri written by Arabic script
    ks_Arab = 1120
    # Represents the Kazakh language as spoken in Kazakhstan
    kk_KZ = 1087
    # Represents the locale for Khmer (Khmer) as used in Cambodia.
    km_KH = 1107
    # Indian Konkani language.
    kok_IN = 1111
    # Korean (South Korea)
    ko_KR = 1042
    # Kyrgyz (Kyrgyzstan).
    ky_KG = 1088
    # K'iche' in Guatemala
    qut_GT = 1158
    # Represents the locale for Rwanda using the Kinyarwanda language.
    rw_RW = 1159
    # Lao
    lo_LA = 1108
    # Latin language.
    la_Latn = 1142
    # Represents the locale for Latvian (Latvia).
    lv_LV = 1062
    # Represents the locale for Lithuanian (Lithuania).
    lt_LT = 1063
    # Lower Sorbian in Germany
    dsb_DE = 2094
    # Luxembourgish
    lb_LU = 1134
    # Represents the locale for Macedonian (North Macedonia).
    mk_MK = 1071
    # Malay in Brunei.
    ms_BN = 2110
    # Represents the locale for Malay (Bahasa Melayu) as used in Malaysia.
    ms_MY = 1086
    # Malayalam in Indian.
    ml_IN = 1100
    # Represents the locale for Maltese (Malta).
    mt_MT = 1082
    # Meitei in Indian
    mni_IN = 1112
    # Maori in New Zealand
    mi_NZ = 1153
    # Marathi (mr) as used in India (IN).
    mr_IN = 1102
    # Mapudungun in Chile
    arn_CL = 1146
    # Mongolian (Mongolia).
    mn_MN = 1104
    # Mongolian (China).
    mn_Mong_CN = 2128
    # Nepali (Nepal).
    ne_NP = 1121
    # Indian which is used in Nepal.
    ne_IN = 2145
    # Represents the Norwegian (Bokmål) language as spoken in Norway.
    nb_NO = 1044
    # Nynorsk (Norway).
    nn_NO = 2068
    # Occitan language in France
    oc_FR = 1154
    # Odia language used in India.
    or_IN = 1096
    # Oromo (Ethiopia) written by Ethiopic script.
    om_Ethi_ET = 1138
    # Papiamento in Netherlands Antilles
    pap_AN = 1145
    # Pashto (Afghanistan).
    ps_AF = 1123
    # Persian in Iran
    fa_IR = 1065
    # Polish (Poland)
    pl_PL = 1045
    # Brazilian Portuguese (Brazil)
    pt_BR = 1046
    # European Portuguese (Portugal)
    pt_PT = 2070
    # Punjabi (India)
    pa_IN = 1094
    # Punjabi in Pakistan
    pa_PK = 2118
    # Southern Quechua (Bolivia).
    quz_BO = 1131
    # Gusii (Ecuador)
    guz_EC = 2155
    # Gusii (Peru)
    guz_PE = 3179
    # Romanian (Romania).
    ro_RO = 1048
    # Romanian (Moldova)
    ro_MO = 2072
    # Romansh (Switzerland)
    rm_CH = 1047
    # Russian (Russia)
    ru_RU = 1049
    # Russian (Moldova).
    ru_MO = 2073
    # Inari Sami (Finland)
    smn_FI = 9275
    # Lule Sami (Norway)
    smj_NO = 4155
    # Lule Sami (Sweden) 
    smj_SE = 5179
    # Northern Sami (Finland).
    se_FI = 3131
    # Northern Sami (Norway).
    se_NO = 1083
    # Northern Sami(Sweden).
    se_SE = 2107
    # Skolt Sami (Finland)
    sms_FI = 8251
    # Southern Sami(Norway).
    sma_NO = 6203
    # Southern Sami(Sweden).
    sma_SE = 7227
    # Sanskrit (India)
    sa_IN = 1103
    # Represents the Serbian language using Cyrillic script for Bosnia and Herzegovina.
    sr_Cyrl_BA = 7194
    # Represents the Serbian language using Cyrillic script as spoken in Serbia.
    sr_Cyrl_CS = 3098
    # Represents the Serbian language using Latin script for Bosnia and Herzegovina.
    sr_Latn_BA = 6170
    # Represents the Serbian language using Latin script and the Cyrillic script as used in Serbia.
    sr_Latn_CS = 2074
    # Northern Sotho (South Africa)
    nso_ZA = 1132
    # Tswana (South African).
    tn_ZA = 1074
    # Sindhi (Pakistan) using Arabic alphabet.
    sd_Arab_PK = 2137
    # Sindhi (India) using Devanagari script.
    sd_Deva_IN = 1113
    # Sinhala (Sri Lanka).
    si_LK = 1115
    # Slovak language (Slovakia).
    sk_SK = 1051
    # Slovenian (Slovenia).
    sl_SI = 1060
    # Somali
    so_SO = 1143
    # Spanish (Argentina)
    es_AR = 11274
    # Spanish (Bolivia)
    es_BO = 16394
    # Spanish (Chile)
    es_CL = 13322
    # Spanish (Colombia)
    es_CO = 9226
    # Spanish (Costa Rica)
    es_CR = 5130
    # Spanish (Dominican Republic)
    es_DO = 7178
    # Spanish (Ecuador)
    es_EC = 12298
    # Spanish (El Salvador)
    es_SV = 17418
    # Spanish (Guatemala)
    es_GT = 4106
    # Spanish (Honduras)
    es_HN = 18442
    # Spanish (Mexico)
    es_MX = 2058
    # Spanish (Nicaragua)
    es_NI = 19466
    # Spanish (Panama)
    es_PA = 6154
    # Spanish (Paraguay)
    es_PY = 15370
    # Spanish (Paraguay
    es_PE = 10250
    # Spanish (Puerto Rico)
    es_PR = 20490
    # Spanish (International Sort)
    es_ES = 3082
    # Spanish(Spain Traditional Sort)
    es_ES_tradnl = 1034
    # Spanish(United Sates)
    es_US = 21514
    # Spanish (Uruguay)
    es_UY = 14346
    # Spanish (Venezuela)
    es_VE = 8202
    # Sutu
    st_ZA = 1072
    # Swahili
    sw_KE = 1089
    # Swedish (Finland)
    sv_FI = 2077
    # Swedish (Sweden)
    sv_SE = 1053
    # Syriac
    syr_SY = 1114
    # Tajik
    tg_Cyrl_TJ = 1064
    # Tamazight
    tzm_Arab_MA = 1119
    # Tamazight (Latin)
    tzm_Latn_DZ = 2143
    # Tamil
    ta_IN = 1097
    # Tatar
    tt_RU = 1092
    # Telugu
    te_IN = 1098
    # Thai
    th_TH = 1054
    # Tibetan (PRC)
    bo_CN = 1105
    # Tigrigna (Eritrea)
    ti_ER = 2163
    # Tigrigna (Ethiopia)
    ti_ET = 1139
    # Tsonga
    ts_ZA = 1073
    # Turkish
    tr_TR = 1055
    # Turkmen
    tk_TM = 1090
    # Uyghur in China
    ug_CN = 1152
    # Ukrainian
    uk_UA = 1058
    # Represents Upper Sorbian in German
    hsb_DE = 1070
    # Urdu
    ur_PK = 1056
    # Uzbek (Cyrillic)
    uz_Cyrl_UZ = 2115
    # Uzbek (Latin)
    uz_Latn_UZ = 1091
    # Venda
    ve_ZA = 1075
    # Vietnamese
    vi_VN = 1066
    # Welsh
    cy_GB = 1106
    # Wolof in Senegal.
    wo_SN = 1160
    # Sakha/Yakut in Russian.
    sah_RU = 1157
    # Yi
    ii_CN = 1144
    # Yiddish
    yi_Hebr = 1085
    # Yoruba
    yo_NG = 1130
    # Japanese
    ja_JP = 1041
    moh_CA = 1148
    quz_EC = 2155
    quz_PE = 3179
    bo_BT = 2129
    nl = 19

