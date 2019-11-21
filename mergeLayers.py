import os, fiona
from collections import OrderedDict
from fiona.crs import from_epsg
from shapely.geometry import shape, mapping

import shutil
import glob

import config
import processGadm
import processPopgis
import voronoi

from zipfile import ZipFile

output_root = "compiledDatasets"
output_crs = from_epsg(3832)

if not os.path.exists(output_root):
    os.mkdir(output_root)

for desired_output in config.desired_outputs:
    out_dir = os.path.join(output_root, desired_output["outputName"])

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    code = f"{desired_output['shortName']}_CODE"
    name = f"{desired_output['shortName']}_NAME"
    output_schema = {
       'geometry': 'Unknown',
       'properties': OrderedDict([
            (name, 'str'),
            (code, 'str'),
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

    if "requiresBuffer" in desired_output:

        centroid_schema = {
           'geometry': 'Unknown',
           'properties': OrderedDict([
                (code, 'str')
            ])
        }

        output_3349_buffered = os.path.join(out_dir, f"{desired_output['outputName']}_buffered.shp")
        output_3349_centroids = os.path.join(out_dir, f"{desired_output['outputName']}_centroids.shp")
        output_3349_voronoi = os.path.join(out_dir, f"{desired_output['outputName']}_voronoi.shp")
    
        output_shp_buffered = fiona.open(
            output_3349_buffered,
            'w',
            driver='ESRI Shapefile',
            crs=output_crs,
            encoding='UTF-8',
            schema=output_schema)

        output_centroid_shp = fiona.open(
            output_3349_centroids,
            'w',
            driver='ESRI Shapefile',
            crs=output_crs,
            encoding='UTF-8',
            schema=centroid_schema)

        output_voronoi_shp = fiona.open(
            output_3349_voronoi,
            'w',
            driver='ESRI Shapefile',
            crs=output_crs,
            encoding='UTF-8',
            schema=centroid_schema) 

        centroids = []
        orig_features = []


    for country in config.countries:
        if desired_output["countryConfigKey"] in country:
            admin_level_info = country[desired_output["countryConfigKey"]]

            country_requires_buffering = True
            if "requiresBuffer" in admin_level_info:
                country_requires_buffering = admin_level_info["requiresBuffer"]
            
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
            src_crs = source.crs['init']

            available_source_fields = source.schema['properties'].keys()

            for f in source:
                out_feature = record_converter(f, desired_output, admin_level_info, country, available_source_fields, src_crs)
                out_feature['properties']['LC_AD_TYPE'] = out_feature['properties']['LC_AD_TYPE'].upper()

                output_shp.write(out_feature)
                
                if "requiresBuffer" in desired_output and country_requires_buffering is not False:
                    out_feature["geometry"] = mapping(shape(out_feature["geometry"]).buffer(25000))
                
                if "requiresBuffer" in desired_output:
                    voronoi.create_centroids(out_feature, code, centroids, output_centroid_shp)
                    orig_features.append(out_feature)

            source.close()
        else :
            print(f"No data available: {desired_output['friendlyName']} - {country['countryName']}")

    output_shp.close()
    output_centroid_shp.close()

    if "requiresBuffer" in desired_output:
        centroid_index = voronoi.create_index_for_centroids(centroids)

        points = [
            [f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1]]
            for index, f in enumerate(centroids)
        ]

        regions, vertices = voronoi.voronoi_finite_polygons_2d(points, 1000000)

        out_regions = []
        for i, region in enumerate(regions):
            out = []
            for v in region:
                out.append([vertices[v][0], vertices[v][1]])

            out_region = {
                "type": "Feature",
                "properties": {
                    code: None
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [out]
                }
            }
            voronoi.get_code_for_voronoi_region(out_region, centroids, centroid_index, code)
            if out_region["properties"][code] is not None:
                out_regions.append(out_region)
                output_voronoi_shp.write(out_region)


        output_voronoi_shp.close()

        voronoi.clip_orig_by_voronoi(orig_features, out_regions, output_shp_buffered, code, desired_output['countryConfigKey'])
      
        output_shp_buffered.close()
    
    shp_name = f"{desired_output['outputName']}.shp"
    shp_components = glob.glob(f"{out_dir}/{desired_output['outputName']}*")
    with ZipFile(f"{out_dir}/{desired_output['outputName']}.zip", 'w') as myzip:
        for component in shp_components:
            myzip.write(component, os.path.basename(component))

