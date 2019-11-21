from countryConfig.americanSamoa import american_samoa
from countryConfig.cookIslands import cook_islands
from countryConfig.fiji import fiji
from countryConfig.frenchPolynesia import french_polynesia
from countryConfig.guam import guam
from countryConfig.kiribati import kiribati
from countryConfig.marshallIslands import marshall_islands
from countryConfig.micronesia import micronesia
from countryConfig.nauru import nauru
from countryConfig.newCaledonia import new_caledonia
from countryConfig.niue import niue
from countryConfig.northernMarianaIslands import northern_mariana
from countryConfig.palau import palau
from countryConfig.papuaNewGuinea import papua_new_guinea
from countryConfig.samoa import samoa
from countryConfig.solomons import solomons
from countryConfig.tokelau import tokelau
from countryConfig.tonga import tonga
from countryConfig.tuvalu import tuvalu
from countryConfig.vanuatu import vanuatu
from countryConfig.wallisFutuna import wallis_futuna


desired_outputs = [
    {
        "friendlyName": "Level Of Detail - Sub-Country 1",
        "outputName": "subCountry1",
        "countryConfigKey": 'subCountry1',
        "levelCode": 1,
        "shortName": "SC1",
        "description": "Sub-national boundaries (level 1) across the South Pacific",
        "requiresBuffer": 25
    },
    {
        "friendlyName": "Level Of Detail - Sub-Country 2",
        "outputName": "subCountry2",
        "countryConfigKey": 'subCountry2',
        "levelCode": 2,
        "shortName": "SC2",
        "description": "Sub-national boundaries (level 2) across the South Pacific"
    },
    {
        "friendlyName": "Level Of Detail - Sub-Country 3",
        "outputName": "subCountry3",
        "countryConfigKey": 'subCountry3',
        "levelCode": 3,
        "shortName": "SC3",
        "description": "Sub-national boundaries (level 3) across the South Pacific"
    }
]

# desired_outputs = [
#     {
#         "friendlyName": "Admin Level 1",
#         "outputName": "adminLevel1",
#         "countryConfigKey": 'adminLevel1',
#         "levelCode": 1,
#         "shortName": "AL1",
#         "description": "Admin Level 1 Boundaries across the south pacific"
#     },
#     {
#         "friendlyName": "Admin Level 2",
#         "outputName": "adminLevel2",
#         "countryConfigKey": 'adminLevel2',
#         "levelCode": 2,
#         "shortName": "AL2",
#         "description": "Admin Level 2 Boundaries across the south pacific"
#     },
#     {
#         "friendlyName": "Admin Level 3",
#         "outputName": "adminLevel3",
#         "countryConfigKey": 'adminLevel3',
#         "levelCode": 3,
#         "shortName": "AL3",
#         "description": "Admin Level 3 Boundaries across the south pacific"
#     }
# ]

countries = [
    american_samoa,
    cook_islands,
    fiji,
    french_polynesia,
    guam,
    kiribati,
    marshall_islands,
    micronesia,
    nauru,
    new_caledonia,
    niue,
    northern_mariana,
    palau,
    papua_new_guinea,
    samoa,
    solomons,
    tokelau,
    tonga,
    tuvalu,
    vanuatu,
    wallis_futuna
]

def get_country_config_by_country_code(country_code):
    for country in countries:
        if country_code == country['countryIsoAlpha3Code']:
            return country
