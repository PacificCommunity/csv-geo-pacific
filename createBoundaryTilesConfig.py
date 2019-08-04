import json
import config

def getAliases(region_mapping_data, layer_name):
    return region_mapping_data["regionMapping"][layer_name]['aliases']

json_file = open('compiledDatasets/regionMapping.json')
region_mapping_data = json.load(json_file)

boundary_types = {}
for layer in config.desired_outputs:
    boundary_types[layer['shortName']] = {
        "shapeNames": {
            f"{layer['outputName']}.zip": f"{layer['outputName']}.shp"
        },
        "regionTypes": {
            layer['shortName']: {
                "regionProp": f"{layer['shortName']}_CODE",
                "nameProp": f"{layer['shortName']}_NAME",
                "aliases": getAliases(region_mapping_data, layer['shortName'])
            }
            # f"{layer['shortName']}_NAME": {
            #     "regionProp": f"{layer['shortName']}_NAME",
            #     "nameProp": f"{layer['shortName']}_NAME",
            #     "aliases": getAliases(region_mapping_data, f"{layer['shortName']}_NAME")
            # }
        }
    }

with open('boundaryTypes.json', 'w') as outfile:  
    json.dump(boundary_types, outfile, indent=2)

