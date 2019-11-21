import os
from collections import OrderedDict
from fiona.transform import transform_geom

def get_data_path(country, desired_output_code):
    return os.path.join(
        "srcDatasets",
        "gadm",
        country["countryIsoAlpha3Code"],
        f"gadm36_{country['countryIsoAlpha3Code']}_{desired_output_code}.shp"
    )


def convertGdamId(gdam_id, gadm_level):
    if gadm_level == 1: return gdam_id.split('.', 1)[1].replace(f"_1", "")
    if gadm_level == 2 or gadm_level == 3: return gdam_id.split('.', 1)[1].replace(f"_1", "").replace('.', '')


def record_converter(record, desired_output, admin_level_info, country_info, available_fields, src_crs):
    id = convertGdamId(record['properties'][f"GID_{desired_output['levelCode']}"], desired_output['levelCode'])
    return {
        'geometry': transform_geom(src_crs, "EPSG:3832", record['geometry']),
        'properties': OrderedDict([
            (f"{desired_output['shortName']}_NAME", record['properties'][f"NAME_{desired_output['levelCode']}"]),
            (f"{desired_output['shortName']}_CODE", f"{country_info['countryIsoAlpha3Code']}-{id}"),
            ('CNTRY_ISO3', country_info['countryIsoAlpha3Code']),
            ('LC_AD_TYPE', admin_level_info['localName']),
            ('SRC_DS', 'GADM')
        ])
    }
