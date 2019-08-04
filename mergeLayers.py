import os, fiona
from collections import OrderedDict
from fiona.crs import from_epsg
import shutil
import glob

import config
import processGadm
import processPopgis
from zipfile import ZipFile

output_root = "compiledDatasets"
output_crs = from_epsg(3349)

if not os.path.exists(output_root):
    os.mkdir(output_root)

for desired_output in config.desired_outputs:
    out_dir = os.path.join(output_root, desired_output["outputName"])

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    output_schema = {
       'geometry': 'Unknown',
       'properties': OrderedDict([
            (f"{desired_output['shortName']}_NAME", 'str'),
            (f"{desired_output['shortName']}_CODE", 'str'),
            ('CNTRY_ISO3', 'str'),
            ('LC_AD_TYPE', 'str'),
            ('SRC_DS', 'str')
        ])
    }

    output_3349 = os.path.join(out_dir, f"{desired_output['outputName']}.shp")
    output_shp = fiona.open(
        output_3349,
        'w',
        driver='ESRI Shapefile',
        crs=output_crs,
        encoding='UTF-8',
        schema=output_schema)
    for country in config.countries:
        if desired_output["countryConfigKey"] in country:
            admin_level_info = country[desired_output["countryConfigKey"]]

            input_data_path = None
            record_converter = None

            if admin_level_info["bestDatasource"] == "popgis":
                input_data_path = processPopgis.get_data_path(admin_level_info['popgisShpSource']) 
                record_converter = processPopgis.record_converter

            if admin_level_info["bestDatasource"] == "gadm":
                if admin_level_info["gadmLevel"]:
                    desired_output['levelCode'] = admin_level_info["gadmLevel"]
                
                input_data_path = processGadm.get_data_path(country, desired_output['levelCode'])
                record_converter = processGadm.record_converter

            source = fiona.open(input_data_path, 'r')
            src_crs = None
            if admin_level_info["bestDatasource"] == "popgis":
                src_crs = source.crs['init']

            if admin_level_info["bestDatasource"] == "gadm":
                src_crs = 'EPSG:4326'

            available_source_fields = source.schema['properties'].keys()
            
            for f in source:
                out_feature = record_converter(f, desired_output, admin_level_info, country, available_source_fields, src_crs)
                out_feature['properties']['LC_AD_TYPE'] = out_feature['properties']['LC_AD_TYPE'].upper()
                output_shp.write(out_feature)
            source.close()
        else :
            print(f"No data available: {desired_output['friendlyName']} - {country['countryName']}")

    output_shp.close()

    shp_name = f"{desired_output['outputName']}.shp"
    shp_compontents = glob.glob(f"{out_dir}/{desired_output['outputName']}*")
        # print(os.path.basename(component))
    # print(shp_compontents)
    with ZipFile(f"{out_dir}/{desired_output['outputName']}.zip", 'w') as myzip:
        for component in shp_compontents:
            myzip.write(component, os.path.basename(component))

       


