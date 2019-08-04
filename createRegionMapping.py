import json
import config
import os

data = {
    "regionMapping": {}
}


def createRegionMapping(newLayerName, description, shortName, nameOrCode):
    return {
        "layerName": newLayerName,
        "description": description,
        "server": f"http://localhost:8000/{newLayerName}/{{z}}/{{x}}/{{y}}.pbf",
        "serverType": "MVT",
        "serverMaxNativeZoom": 12,
        "serverMinZoom": 0,
        "serverMaxZoom": 28,
        "regionIdsFile": f"/data/regionids/region_map-{newLayerName}.json",
        "regionProp": f"{shortName}_{nameOrCode}",
        "nameProp": f"{shortName}_NAME",
        "aliases": [
            f"{shortName}{nameOrCode}"
        ],
        "bbox": [
            112.92111395199997,
            -43.740509602999985,
            159.10921900799997,
            -9.142175976999999
        ]
    }

for output in config.desired_outputs:

    output_shp = os.path.join("compiledDatasets", output["outputName"], f"{output['outputName']}.shp")

    # Create the region mapping based on codes
    codeBasedLayer = f"{output['shortName']}"
    new_region_mapping = createRegionMapping(codeBasedLayer, output['description'], output['shortName'], 'CODE')
    for country in config.countries:
        if output["countryConfigKey"] not in country:
            continue
        admin_level_info = country[output["countryConfigKey"]]
        new_region_mapping['aliases'].append(f"{country['countryIsoAlpha3Code']}_{output['shortName']}_CODE")
        new_region_mapping['aliases'].append(f"{country['countryIsoAlpha3Code']}_{admin_level_info['localName'].upper().replace(' ', '_')}_CODE")
    data['regionMapping'][codeBasedLayer] = new_region_mapping


    # # Create the region mappings based on name
    # nameBasedLayer = f"{output['shortName']}_NAME"
    # new_region_mapping = createRegionMapping(nameBasedLayer, output['description'], output['shortName'], 'NAME')
    # for country in config.countries:
    #     if output["countryConfigKey"] not in country:
    #         continue
    #     admin_level_info = country[output["countryConfigKey"]]
    #     new_region_mapping['aliases'].append(f"{country['countryIsoAlpha3Code']}_{output['shortName']}_NAME")
    #     new_region_mapping['aliases'].append(f"{country['countryIsoAlpha3Code']}_{admin_level_info['localName'].upper()}_NAME") 
    # data['regionMapping'][nameBasedLayer] = new_region_mapping


with open('compiledDatasets/regionMapping.json', 'w') as outfile:  
    json.dump(data, outfile, indent=2)
 