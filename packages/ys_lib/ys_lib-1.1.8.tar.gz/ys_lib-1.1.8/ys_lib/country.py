# -*- coding: utf-8 -*-
"""全球国家及地区枚举"""
from collections import namedtuple
from enum import auto, Enum
from typing import Dict, List
from .base import ByKey

# https://www.nationsonline.org/oneworld/country_code_list.htm

field_names: List[str] = ["a3_code", "a2_code", "un_code", "en_name"]
CountryDetail = namedtuple(typename="CountryDetail", field_names=field_names)
tsv: str = """
AFG\tAF\t004\tAfghanistan
ALA\tAX\t248\tAland Islands
ALB\tAL\t008\tAlbania
DZA\tDZ\t012\tAlgeria
ASM\tAS\t016\tAmerican Samoa
AND\tAD\t020\tAndorra
AGO\tAO\t024\tAngola
AIA\tAI\t660\tAnguilla
ATA\tAQ\t010\tAntarctica
ATG\tAG\t028\tAntigua and Barbuda
ARG\tAR\t032\tArgentina
ARM\tAM\t051\tArmenia
ABW\tAW\t533\tAruba
AUS\tAU\t036\tAustralia
AUT\tAT\t040\tAustria
AZE\tAZ\t031\tAzerbaijan
BHS\tBS\t044\tBahamas
BHR\tBH\t048\tBahrain
BGD\tBD\t050\tBangladesh
BRB\tBB\t052\tBarbados
BLR\tBY\t112\tBelarus
BEL\tBE\t056\tBelgium
BLZ\tBZ\t084\tBelize
BEN\tBJ\t204\tBenin
BMU\tBM\t060\tBermuda
BTN\tBT\t064\tBhutan
BOL\tBO\t068\tBolivia
BIH\tBA\t070\tBosnia and Herzegovina
BWA\tBW\t072\tBotswana
BVT\tBV\t074\tBouvet Island
BRA\tBR\t076\tBrazil
VGB\tVG\t092\tBritish Virgin Islands
IOT\tIO\t086\tBritish Indian Ocean Territory
BRN\tBN\t096\tBrunei Darussalam
BGR\tBG\t100\tBulgaria
BFA\tBF\t854\tBurkina Faso
BDI\tBI\t108\tBurundi
KHM\tKH\t116\tCambodia
CMR\tCM\t120\tCameroon
CAN\tCA\t124\tCanada
CPV\tCV\t132\tCape Verde
CYM\tKY\t136\tCayman Islands
CAF\tCF\t140\tCentral African Republic
TCD\tTD\t148\tChad
CHL\tCL\t152\tChile
CHN\tCN\t156\tChina
HKG\tHK\t344\tHong Kong, SAR China
MAC\tMO\t446\tMacao, SAR China
CXR\tCX\t162\tChristmas Island
CCK\tCC\t166\tCocos (Keeling) Islands
COL\tCO\t170\tColombia
COM\tKM\t174\tComoros
COG\tCG\t178\tCongo (Brazzaville)
COD\tCD\t180\tCongo, (Kinshasa)
COK\tCK\t184\tCook Islands
CRI\tCR\t188\tCosta Rica
CIV\tCI\t384\tCôte d'Ivoire
HRV\tHR\t191\tCroatia
CUB\tCU\t192\tCuba
CYP\tCY\t196\tCyprus
CZE\tCZ\t203\tCzech Republic
DNK\tDK\t208\tDenmark
DJI\tDJ\t262\tDjibouti
DMA\tDM\t212\tDominica
DOM\tDO\t214\tDominican Republic
ECU\tEC\t218\tEcuador
EGY\tEG\t818\tEgypt
SLV\tSV\t222\tEl Salvador
GNQ\tGQ\t226\tEquatorial Guinea
ERI\tER\t232\tEritrea
EST\tEE\t233\tEstonia
ETH\tET\t231\tEthiopia
FLK\tFK\t238\tFalkland Islands (Malvinas)
FRO\tFO\t234\tFaroe Islands
FJI\tFJ\t242\tFiji
FIN\tFI\t246\tFinland
FRA\tFR\t250\tFrance
GUF\tGF\t254\tFrench Guiana
PYF\tPF\t258\tFrench Polynesia
ATF\tTF\t260\tFrench Southern Territories
GAB\tGA\t266\tGabon
GMB\tGM\t270\tGambia
GEO\tGE\t268\tGeorgia
DEU\tDE\t276\tGermany
GHA\tGH\t288\tGhana
GIB\tGI\t292\tGibraltar
GRC\tGR\t300\tGreece
GRL\tGL\t304\tGreenland
GRD\tGD\t308\tGrenada
GLP\tGP\t312\tGuadeloupe
GUM\tGU\t316\tGuam
GTM\tGT\t320\tGuatemala
GGY\tGG\t831\tGuernsey
GIN\tGN\t324\tGuinea
GNB\tGW\t624\tGuinea-Bissau
GUY\tGY\t328\tGuyana
HTI\tHT\t332\tHaiti
HMD\tHM\t334\tHeard and Mcdonald Islands
VAT\tVA\t336\tHoly See (Vatican City State)
HND\tHN\t340\tHonduras
HUN\tHU\t348\tHungary
ISL\tIS\t352\tIceland
IND\tIN\t356\tIndia
IDN\tID\t360\tIndonesia
IRN\tIR\t364\tIran, Islamic Republic of
IRQ\tIQ\t368\tIraq
IRL\tIE\t372\tIreland
IMN\tIM\t833\tIsle of Man
ISR\tIL\t376\tIsrael
ITA\tIT\t380\tItaly
JAM\tJM\t388\tJamaica
JPN\tJP\t392\tJapan
JEY\tJE\t832\tJersey
JOR\tJO\t400\tJordan
KAZ\tKZ\t398\tKazakhstan
KEN\tKE\t404\tKenya
KIR\tKI\t296\tKiribati
PRK\tKP\t408\tKorea (North)
KOR\tKR\t410\tKorea (South)
KWT\tKW\t414\tKuwait
KGZ\tKG\t417\tKyrgyzstan
LAO\tLA\t418\tLao PDR
LVA\tLV\t428\tLatvia
LBN\tLB\t422\tLebanon
LSO\tLS\t426\tLesotho
LBR\tLR\t430\tLiberia
LBY\tLY\t434\tLibya
LIE\tLI\t438\tLiechtenstein
LTU\tLT\t440\tLithuania
LUX\tLU\t442\tLuxembourg
MKD\tMK\t807\tMacedonia, Republic of
MDG\tMG\t450\tMadagascar
MWI\tMW\t454\tMalawi
MYS\tMY\t458\tMalaysia
MDV\tMV\t462\tMaldives
MLI\tML\t466\tMali
MLT\tMT\t470\tMalta
MHL\tMH\t584\tMarshall Islands
MTQ\tMQ\t474\tMartinique
MRT\tMR\t478\tMauritania
MUS\tMU\t480\tMauritius
MYT\tYT\t175\tMayotte
MEX\tMX\t484\tMexico
FSM\tFM\t583\tMicronesia, Federated States of
MDA\tMD\t498\tMoldova
MCO\tMC\t492\tMonaco
MNG\tMN\t496\tMongolia
MNE\tME\t499\tMontenegro
MSR\tMS\t500\tMontserrat
MAR\tMA\t504\tMorocco
MOZ\tMZ\t508\tMozambique
MMR\tMM\t104\tMyanmar
NAM\tNA\t516\tNamibia
NRU\tNR\t520\tNauru
NPL\tNP\t524\tNepal
NLD\tNL\t528\tNetherlands
ANT\tAN\t530\tNetherlands Antilles
NCL\tNC\t540\tNew Caledonia
NZL\tNZ\t554\tNew Zealand
NIC\tNI\t558\tNicaragua
NER\tNE\t562\tNiger
NGA\tNG\t566\tNigeria
NIU\tNU\t570\tNiue
NFK\tNF\t574\tNorfolk Island
MNP\tMP\t580\tNorthern Mariana Islands
NOR\tNO\t578\tNorway
OMN\tOM\t512\tOman
PAK\tPK\t586\tPakistan
PLW\tPW\t585\tPalau
PSE\tPS\t275\tPalestinian Territory
PAN\tPA\t591\tPanama
PNG\tPG\t598\tPapua New Guinea
PRY\tPY\t600\tParaguay
PER\tPE\t604\tPeru
PHL\tPH\t608\tPhilippines
PCN\tPN\t612\tPitcairn
POL\tPL\t616\tPoland
PRT\tPT\t620\tPortugal
PRI\tPR\t630\tPuerto Rico
QAT\tQA\t634\tQatar
REU\tRE\t638\tRéunion
ROU\tRO\t642\tRomania
RUS\tRU\t643\tRussian Federation
RWA\tRW\t646\tRwanda
BLM\tBL\t652\tSaint-Barthélemy
SHN\tSH\t654\tSaint Helena
KNA\tKN\t659\tSaint Kitts and Nevis
LCA\tLC\t662\tSaint Lucia
MAF\tMF\t663\tSaint-Martin (French part)
SPM\tPM\t666\tSaint Pierre and Miquelon
VCT\tVC\t670\tSaint Vincent and Grenadines
WSM\tWS\t882\tSamoa
SMR\tSM\t674\tSan Marino
STP\tST\t678\tSao Tome and Principe
SAU\tSA\t682\tSaudi Arabia
SEN\tSN\t686\tSenegal
SRB\tRS\t688\tSerbia
SYC\tSC\t690\tSeychelles
SLE\tSL\t694\tSierra Leone
SGP\tSG\t702\tSingapore
SVK\tSK\t703\tSlovakia
SVN\tSI\t705\tSlovenia
SLB\tSB\t090\tSolomon Islands
SOM\tSO\t706\tSomalia
ZAF\tZA\t710\tSouth Africa
SGS\tGS\t239\tSouth Georgia and the South Sandwich Islands
SSD\tSS\t728\tSouth Sudan
ESP\tES\t724\tSpain
LKA\tLK\t144\tSri Lanka
SDN\tSD\t736\tSudan
SUR\tSR\t740\tSuriname
SJM\tSJ\t744\tSvalbard and Jan Mayen Islands
SWZ\tSZ\t748\tSwaziland
SWE\tSE\t752\tSweden
CHE\tCH\t756\tSwitzerland
SYR\tSY\t760\tSyrian Arab Republic (Syria)
TWN\tTW\t158\tTaiwan, Republic of China
TJK\tTJ\t762\tTajikistan
TZA\tTZ\t834\tTanzania, United Republic of
THA\tTH\t764\tThailand
TLS\tTL\t626\tTimor-Leste
TGO\tTG\t768\tTogo
TKL\tTK\t772\tTokelau
TON\tTO\t776\tTonga
TTO\tTT\t780\tTrinidad and Tobago
TUN\tTN\t788\tTunisia
TUR\tTR\t792\tTurkey
TKM\tTM\t795\tTurkmenistan
TCA\tTC\t796\tTurks and Caicos Islands
TUV\tTV\t798\tTuvalu
UGA\tUG\t800\tUganda
UKR\tUA\t804\tUkraine
ARE\tAE\t784\tUnited Arab Emirates
GBR\tGB\t826\tUnited Kingdom
USA\tUS\t840\tUnited States of America
UMI\tUM\t581\tUS Minor Outlying Islands
URY\tUY\t858\tUruguay
UZB\tUZ\t860\tUzbekistan
VUT\tVU\t548\tVanuatu
VEN\tVE\t862\tVenezuela (Bolivarian Republic)
VNM\tVN\t704\tViet Nam
VIR\tVI\t850\tVirgin Islands, US
WLF\tWF\t876\tWallis and Futuna Islands
ESH\tEH\t732\tWestern Sahara
YEM\tYE\t887\tYemen
ZMB\tZM\t894\tZambia
ZWE\tZW\t716\tZimbabwe
"""
# a3_code   Alpha 3 Code
# a2_code   Alpha 2 Code
# un_code   UN Code
# en_name   Country
Items: List[CountryDetail] = [CountryDetail(*line.strip().split("\t")) for line in tsv.splitlines() if line]


class ByA2Code(ByKey):
    map: Dict[str, CountryDetail] = {getattr(item, field_names[1]): item for item in Items}


class ByA3Code(ByKey):
    map: Dict[str, CountryDetail] = {getattr(item, field_names[0]): item for item in Items}


class CountryA3(Enum):
    """三字母国家代码枚举"""

    AFG = ByA3Code.map['AFG']
    ALA = ByA3Code.map['ALA']
    ALB = ByA3Code.map['ALB']
    DZA = ByA3Code.map['DZA']
    ASM = ByA3Code.map['ASM']
    AND = ByA3Code.map['AND']
    AGO = ByA3Code.map['AGO']
    AIA = ByA3Code.map['AIA']
    ATA = ByA3Code.map['ATA']
    ATG = ByA3Code.map['ATG']
    ARG = ByA3Code.map['ARG']
    ARM = ByA3Code.map['ARM']
    ABW = ByA3Code.map['ABW']
    AUS = ByA3Code.map['AUS']
    AUT = ByA3Code.map['AUT']
    AZE = ByA3Code.map['AZE']
    BHS = ByA3Code.map['BHS']
    BHR = ByA3Code.map['BHR']
    BGD = ByA3Code.map['BGD']
    BRB = ByA3Code.map['BRB']
    BLR = ByA3Code.map['BLR']
    BEL = ByA3Code.map['BEL']
    BLZ = ByA3Code.map['BLZ']
    BEN = ByA3Code.map['BEN']
    BMU = ByA3Code.map['BMU']
    BTN = ByA3Code.map['BTN']
    BOL = ByA3Code.map['BOL']
    BIH = ByA3Code.map['BIH']
    BWA = ByA3Code.map['BWA']
    BVT = ByA3Code.map['BVT']
    BRA = ByA3Code.map['BRA']
    VGB = ByA3Code.map['VGB']
    IOT = ByA3Code.map['IOT']
    BRN = ByA3Code.map['BRN']
    BGR = ByA3Code.map['BGR']
    BFA = ByA3Code.map['BFA']
    BDI = ByA3Code.map['BDI']
    KHM = ByA3Code.map['KHM']
    CMR = ByA3Code.map['CMR']
    CAN = ByA3Code.map['CAN']
    CPV = ByA3Code.map['CPV']
    CYM = ByA3Code.map['CYM']
    CAF = ByA3Code.map['CAF']
    TCD = ByA3Code.map['TCD']
    CHL = ByA3Code.map['CHL']
    CHN = ByA3Code.map['CHN']
    HKG = ByA3Code.map['HKG']
    MAC = ByA3Code.map['MAC']
    CXR = ByA3Code.map['CXR']
    CCK = ByA3Code.map['CCK']
    COL = ByA3Code.map['COL']
    COM = ByA3Code.map['COM']
    COG = ByA3Code.map['COG']
    COD = ByA3Code.map['COD']
    COK = ByA3Code.map['COK']
    CRI = ByA3Code.map['CRI']
    CIV = ByA3Code.map['CIV']
    HRV = ByA3Code.map['HRV']
    CUB = ByA3Code.map['CUB']
    CYP = ByA3Code.map['CYP']
    CZE = ByA3Code.map['CZE']
    DNK = ByA3Code.map['DNK']
    DJI = ByA3Code.map['DJI']
    DMA = ByA3Code.map['DMA']
    DOM = ByA3Code.map['DOM']
    ECU = ByA3Code.map['ECU']
    EGY = ByA3Code.map['EGY']
    SLV = ByA3Code.map['SLV']
    GNQ = ByA3Code.map['GNQ']
    ERI = ByA3Code.map['ERI']
    EST = ByA3Code.map['EST']
    ETH = ByA3Code.map['ETH']
    FLK = ByA3Code.map['FLK']
    FRO = ByA3Code.map['FRO']
    FJI = ByA3Code.map['FJI']
    FIN = ByA3Code.map['FIN']
    FRA = ByA3Code.map['FRA']
    GUF = ByA3Code.map['GUF']
    PYF = ByA3Code.map['PYF']
    ATF = ByA3Code.map['ATF']
    GAB = ByA3Code.map['GAB']
    GMB = ByA3Code.map['GMB']
    GEO = ByA3Code.map['GEO']
    DEU = ByA3Code.map['DEU']
    GHA = ByA3Code.map['GHA']
    GIB = ByA3Code.map['GIB']
    GRC = ByA3Code.map['GRC']
    GRL = ByA3Code.map['GRL']
    GRD = ByA3Code.map['GRD']
    GLP = ByA3Code.map['GLP']
    GUM = ByA3Code.map['GUM']
    GTM = ByA3Code.map['GTM']
    GGY = ByA3Code.map['GGY']
    GIN = ByA3Code.map['GIN']
    GNB = ByA3Code.map['GNB']
    GUY = ByA3Code.map['GUY']
    HTI = ByA3Code.map['HTI']
    HMD = ByA3Code.map['HMD']
    VAT = ByA3Code.map['VAT']
    HND = ByA3Code.map['HND']
    HUN = ByA3Code.map['HUN']
    ISL = ByA3Code.map['ISL']
    IND = ByA3Code.map['IND']
    IDN = ByA3Code.map['IDN']
    IRN = ByA3Code.map['IRN']
    IRQ = ByA3Code.map['IRQ']
    IRL = ByA3Code.map['IRL']
    IMN = ByA3Code.map['IMN']
    ISR = ByA3Code.map['ISR']
    ITA = ByA3Code.map['ITA']
    JAM = ByA3Code.map['JAM']
    JPN = ByA3Code.map['JPN']
    JEY = ByA3Code.map['JEY']
    JOR = ByA3Code.map['JOR']
    KAZ = ByA3Code.map['KAZ']
    KEN = ByA3Code.map['KEN']
    KIR = ByA3Code.map['KIR']
    PRK = ByA3Code.map['PRK']
    KOR = ByA3Code.map['KOR']
    KWT = ByA3Code.map['KWT']
    KGZ = ByA3Code.map['KGZ']
    LAO = ByA3Code.map['LAO']
    LVA = ByA3Code.map['LVA']
    LBN = ByA3Code.map['LBN']
    LSO = ByA3Code.map['LSO']
    LBR = ByA3Code.map['LBR']
    LBY = ByA3Code.map['LBY']
    LIE = ByA3Code.map['LIE']
    LTU = ByA3Code.map['LTU']
    LUX = ByA3Code.map['LUX']
    MKD = ByA3Code.map['MKD']
    MDG = ByA3Code.map['MDG']
    MWI = ByA3Code.map['MWI']
    MYS = ByA3Code.map['MYS']
    MDV = ByA3Code.map['MDV']
    MLI = ByA3Code.map['MLI']
    MLT = ByA3Code.map['MLT']
    MHL = ByA3Code.map['MHL']
    MTQ = ByA3Code.map['MTQ']
    MRT = ByA3Code.map['MRT']
    MUS = ByA3Code.map['MUS']
    MYT = ByA3Code.map['MYT']
    MEX = ByA3Code.map['MEX']
    FSM = ByA3Code.map['FSM']
    MDA = ByA3Code.map['MDA']
    MCO = ByA3Code.map['MCO']
    MNG = ByA3Code.map['MNG']
    MNE = ByA3Code.map['MNE']
    MSR = ByA3Code.map['MSR']
    MAR = ByA3Code.map['MAR']
    MOZ = ByA3Code.map['MOZ']
    MMR = ByA3Code.map['MMR']
    NAM = ByA3Code.map['NAM']
    NRU = ByA3Code.map['NRU']
    NPL = ByA3Code.map['NPL']
    NLD = ByA3Code.map['NLD']
    ANT = ByA3Code.map['ANT']
    NCL = ByA3Code.map['NCL']
    NZL = ByA3Code.map['NZL']
    NIC = ByA3Code.map['NIC']
    NER = ByA3Code.map['NER']
    NGA = ByA3Code.map['NGA']
    NIU = ByA3Code.map['NIU']
    NFK = ByA3Code.map['NFK']
    MNP = ByA3Code.map['MNP']
    NOR = ByA3Code.map['NOR']
    OMN = ByA3Code.map['OMN']
    PAK = ByA3Code.map['PAK']
    PLW = ByA3Code.map['PLW']
    PSE = ByA3Code.map['PSE']
    PAN = ByA3Code.map['PAN']
    PNG = ByA3Code.map['PNG']
    PRY = ByA3Code.map['PRY']
    PER = ByA3Code.map['PER']
    PHL = ByA3Code.map['PHL']
    PCN = ByA3Code.map['PCN']
    POL = ByA3Code.map['POL']
    PRT = ByA3Code.map['PRT']
    PRI = ByA3Code.map['PRI']
    QAT = ByA3Code.map['QAT']
    REU = ByA3Code.map['REU']
    ROU = ByA3Code.map['ROU']
    RUS = ByA3Code.map['RUS']
    RWA = ByA3Code.map['RWA']
    BLM = ByA3Code.map['BLM']
    SHN = ByA3Code.map['SHN']
    KNA = ByA3Code.map['KNA']
    LCA = ByA3Code.map['LCA']
    MAF = ByA3Code.map['MAF']
    SPM = ByA3Code.map['SPM']
    VCT = ByA3Code.map['VCT']
    WSM = ByA3Code.map['WSM']
    SMR = ByA3Code.map['SMR']
    STP = ByA3Code.map['STP']
    SAU = ByA3Code.map['SAU']
    SEN = ByA3Code.map['SEN']
    SRB = ByA3Code.map['SRB']
    SYC = ByA3Code.map['SYC']
    SLE = ByA3Code.map['SLE']
    SGP = ByA3Code.map['SGP']
    SVK = ByA3Code.map['SVK']
    SVN = ByA3Code.map['SVN']
    SLB = ByA3Code.map['SLB']
    SOM = ByA3Code.map['SOM']
    ZAF = ByA3Code.map['ZAF']
    SGS = ByA3Code.map['SGS']
    SSD = ByA3Code.map['SSD']
    ESP = ByA3Code.map['ESP']
    LKA = ByA3Code.map['LKA']
    SDN = ByA3Code.map['SDN']
    SUR = ByA3Code.map['SUR']
    SJM = ByA3Code.map['SJM']
    SWZ = ByA3Code.map['SWZ']
    SWE = ByA3Code.map['SWE']
    CHE = ByA3Code.map['CHE']
    SYR = ByA3Code.map['SYR']
    TWN = ByA3Code.map['TWN']
    TJK = ByA3Code.map['TJK']
    TZA = ByA3Code.map['TZA']
    THA = ByA3Code.map['THA']
    TLS = ByA3Code.map['TLS']
    TGO = ByA3Code.map['TGO']
    TKL = ByA3Code.map['TKL']
    TON = ByA3Code.map['TON']
    TTO = ByA3Code.map['TTO']
    TUN = ByA3Code.map['TUN']
    TUR = ByA3Code.map['TUR']
    TKM = ByA3Code.map['TKM']
    TCA = ByA3Code.map['TCA']
    TUV = ByA3Code.map['TUV']
    UGA = ByA3Code.map['UGA']
    UKR = ByA3Code.map['UKR']
    ARE = ByA3Code.map['ARE']
    GBR = ByA3Code.map['GBR']
    USA = ByA3Code.map['USA']
    UMI = ByA3Code.map['UMI']
    URY = ByA3Code.map['URY']
    UZB = ByA3Code.map['UZB']
    VUT = ByA3Code.map['VUT']
    VEN = ByA3Code.map['VEN']
    VNM = ByA3Code.map['VNM']
    VIR = ByA3Code.map['VIR']
    WLF = ByA3Code.map['WLF']
    ESH = ByA3Code.map['ESH']
    YEM = ByA3Code.map['YEM']
    ZMB = ByA3Code.map['ZMB']
    ZWE = ByA3Code.map['ZWE']


class CountryA2(Enum):
    """双字母国家代码枚举"""

    AF = ByA2Code.map['AF']
    AX = ByA2Code.map['AX']
    AL = ByA2Code.map['AL']
    DZ = ByA2Code.map['DZ']
    AS = ByA2Code.map['AS']
    AD = ByA2Code.map['AD']
    AO = ByA2Code.map['AO']
    AI = ByA2Code.map['AI']
    AQ = ByA2Code.map['AQ']
    AG = ByA2Code.map['AG']
    AR = ByA2Code.map['AR']
    AM = ByA2Code.map['AM']
    AW = ByA2Code.map['AW']
    AU = ByA2Code.map['AU']
    AT = ByA2Code.map['AT']
    AZ = ByA2Code.map['AZ']
    BS = ByA2Code.map['BS']
    BH = ByA2Code.map['BH']
    BD = ByA2Code.map['BD']
    BB = ByA2Code.map['BB']
    BY = ByA2Code.map['BY']
    BE = ByA2Code.map['BE']
    BZ = ByA2Code.map['BZ']
    BJ = ByA2Code.map['BJ']
    BM = ByA2Code.map['BM']
    BT = ByA2Code.map['BT']
    BO = ByA2Code.map['BO']
    BA = ByA2Code.map['BA']
    BW = ByA2Code.map['BW']
    BV = ByA2Code.map['BV']
    BR = ByA2Code.map['BR']
    VG = ByA2Code.map['VG']
    IO = ByA2Code.map['IO']
    BN = ByA2Code.map['BN']
    BG = ByA2Code.map['BG']
    BF = ByA2Code.map['BF']
    BI = ByA2Code.map['BI']
    KH = ByA2Code.map['KH']
    CM = ByA2Code.map['CM']
    CA = ByA2Code.map['CA']
    CV = ByA2Code.map['CV']
    KY = ByA2Code.map['KY']
    CF = ByA2Code.map['CF']
    TD = ByA2Code.map['TD']
    CL = ByA2Code.map['CL']
    CN = ByA2Code.map['CN']
    HK = ByA2Code.map['HK']
    MO = ByA2Code.map['MO']
    CX = ByA2Code.map['CX']
    CC = ByA2Code.map['CC']
    CO = ByA2Code.map['CO']
    KM = ByA2Code.map['KM']
    CG = ByA2Code.map['CG']
    CD = ByA2Code.map['CD']
    CK = ByA2Code.map['CK']
    CR = ByA2Code.map['CR']
    CI = ByA2Code.map['CI']
    HR = ByA2Code.map['HR']
    CU = ByA2Code.map['CU']
    CY = ByA2Code.map['CY']
    CZ = ByA2Code.map['CZ']
    DK = ByA2Code.map['DK']
    DJ = ByA2Code.map['DJ']
    DM = ByA2Code.map['DM']
    DO = ByA2Code.map['DO']
    EC = ByA2Code.map['EC']
    EG = ByA2Code.map['EG']
    SV = ByA2Code.map['SV']
    GQ = ByA2Code.map['GQ']
    ER = ByA2Code.map['ER']
    EE = ByA2Code.map['EE']
    ET = ByA2Code.map['ET']
    FK = ByA2Code.map['FK']
    FO = ByA2Code.map['FO']
    FJ = ByA2Code.map['FJ']
    FI = ByA2Code.map['FI']
    FR = ByA2Code.map['FR']
    GF = ByA2Code.map['GF']
    PF = ByA2Code.map['PF']
    TF = ByA2Code.map['TF']
    GA = ByA2Code.map['GA']
    GM = ByA2Code.map['GM']
    GE = ByA2Code.map['GE']
    DE = ByA2Code.map['DE']
    GH = ByA2Code.map['GH']
    GI = ByA2Code.map['GI']
    GR = ByA2Code.map['GR']
    GL = ByA2Code.map['GL']
    GD = ByA2Code.map['GD']
    GP = ByA2Code.map['GP']
    GU = ByA2Code.map['GU']
    GT = ByA2Code.map['GT']
    GG = ByA2Code.map['GG']
    GN = ByA2Code.map['GN']
    GW = ByA2Code.map['GW']
    GY = ByA2Code.map['GY']
    HT = ByA2Code.map['HT']
    HM = ByA2Code.map['HM']
    VA = ByA2Code.map['VA']
    HN = ByA2Code.map['HN']
    HU = ByA2Code.map['HU']
    IS = ByA2Code.map['IS']
    IN = ByA2Code.map['IN']
    ID = ByA2Code.map['ID']
    IR = ByA2Code.map['IR']
    IQ = ByA2Code.map['IQ']
    IE = ByA2Code.map['IE']
    IM = ByA2Code.map['IM']
    IL = ByA2Code.map['IL']
    IT = ByA2Code.map['IT']
    JM = ByA2Code.map['JM']
    JP = ByA2Code.map['JP']
    JE = ByA2Code.map['JE']
    JO = ByA2Code.map['JO']
    KZ = ByA2Code.map['KZ']
    KE = ByA2Code.map['KE']
    KI = ByA2Code.map['KI']
    KP = ByA2Code.map['KP']
    KR = ByA2Code.map['KR']
    KW = ByA2Code.map['KW']
    KG = ByA2Code.map['KG']
    LA = ByA2Code.map['LA']
    LV = ByA2Code.map['LV']
    LB = ByA2Code.map['LB']
    LS = ByA2Code.map['LS']
    LR = ByA2Code.map['LR']
    LY = ByA2Code.map['LY']
    LI = ByA2Code.map['LI']
    LT = ByA2Code.map['LT']
    LU = ByA2Code.map['LU']
    MK = ByA2Code.map['MK']
    MG = ByA2Code.map['MG']
    MW = ByA2Code.map['MW']
    MY = ByA2Code.map['MY']
    MV = ByA2Code.map['MV']
    ML = ByA2Code.map['ML']
    MT = ByA2Code.map['MT']
    MH = ByA2Code.map['MH']
    MQ = ByA2Code.map['MQ']
    MR = ByA2Code.map['MR']
    MU = ByA2Code.map['MU']
    YT = ByA2Code.map['YT']
    MX = ByA2Code.map['MX']
    FM = ByA2Code.map['FM']
    MD = ByA2Code.map['MD']
    MC = ByA2Code.map['MC']
    MN = ByA2Code.map['MN']
    ME = ByA2Code.map['ME']
    MS = ByA2Code.map['MS']
    MA = ByA2Code.map['MA']
    MZ = ByA2Code.map['MZ']
    MM = ByA2Code.map['MM']
    NA = ByA2Code.map['NA']
    NR = ByA2Code.map['NR']
    NP = ByA2Code.map['NP']
    NL = ByA2Code.map['NL']
    AN = ByA2Code.map['AN']
    NC = ByA2Code.map['NC']
    NZ = ByA2Code.map['NZ']
    NI = ByA2Code.map['NI']
    NE = ByA2Code.map['NE']
    NG = ByA2Code.map['NG']
    NU = ByA2Code.map['NU']
    NF = ByA2Code.map['NF']
    MP = ByA2Code.map['MP']
    NO = ByA2Code.map['NO']
    OM = ByA2Code.map['OM']
    PK = ByA2Code.map['PK']
    PW = ByA2Code.map['PW']
    PS = ByA2Code.map['PS']
    PA = ByA2Code.map['PA']
    PG = ByA2Code.map['PG']
    PY = ByA2Code.map['PY']
    PE = ByA2Code.map['PE']
    PH = ByA2Code.map['PH']
    PN = ByA2Code.map['PN']
    PL = ByA2Code.map['PL']
    PT = ByA2Code.map['PT']
    PR = ByA2Code.map['PR']
    QA = ByA2Code.map['QA']
    RE = ByA2Code.map['RE']
    RO = ByA2Code.map['RO']
    RU = ByA2Code.map['RU']
    RW = ByA2Code.map['RW']
    BL = ByA2Code.map['BL']
    SH = ByA2Code.map['SH']
    KN = ByA2Code.map['KN']
    LC = ByA2Code.map['LC']
    MF = ByA2Code.map['MF']
    PM = ByA2Code.map['PM']
    VC = ByA2Code.map['VC']
    WS = ByA2Code.map['WS']
    SM = ByA2Code.map['SM']
    ST = ByA2Code.map['ST']
    SA = ByA2Code.map['SA']
    SN = ByA2Code.map['SN']
    RS = ByA2Code.map['RS']
    SC = ByA2Code.map['SC']
    SL = ByA2Code.map['SL']
    SG = ByA2Code.map['SG']
    SK = ByA2Code.map['SK']
    SI = ByA2Code.map['SI']
    SB = ByA2Code.map['SB']
    SO = ByA2Code.map['SO']
    ZA = ByA2Code.map['ZA']
    GS = ByA2Code.map['GS']
    SS = ByA2Code.map['SS']
    ES = ByA2Code.map['ES']
    LK = ByA2Code.map['LK']
    SD = ByA2Code.map['SD']
    SR = ByA2Code.map['SR']
    SJ = ByA2Code.map['SJ']
    SZ = ByA2Code.map['SZ']
    SE = ByA2Code.map['SE']
    CH = ByA2Code.map['CH']
    SY = ByA2Code.map['SY']
    TW = ByA2Code.map['TW']
    TJ = ByA2Code.map['TJ']
    TZ = ByA2Code.map['TZ']
    TH = ByA2Code.map['TH']
    TL = ByA2Code.map['TL']
    TG = ByA2Code.map['TG']
    TK = ByA2Code.map['TK']
    TO = ByA2Code.map['TO']
    TT = ByA2Code.map['TT']
    TN = ByA2Code.map['TN']
    TR = ByA2Code.map['TR']
    TM = ByA2Code.map['TM']
    TC = ByA2Code.map['TC']
    TV = ByA2Code.map['TV']
    UG = ByA2Code.map['UG']
    UA = ByA2Code.map['UA']
    AE = ByA2Code.map['AE']
    GB = ByA2Code.map['GB']
    US = ByA2Code.map['US']
    UM = ByA2Code.map['UM']
    UY = ByA2Code.map['UY']
    UZ = ByA2Code.map['UZ']
    VU = ByA2Code.map['VU']
    VE = ByA2Code.map['VE']
    VN = ByA2Code.map['VN']
    VI = ByA2Code.map['VI']
    WF = ByA2Code.map['WF']
    EH = ByA2Code.map['EH']
    YE = ByA2Code.map['YE']
    ZM = ByA2Code.map['ZM']
    ZW = ByA2Code.map['ZW']


# 数据完整性和一致性检验
ByA3Code.check(obj=CountryA3)
ByA2Code.check(obj=CountryA2)
