
import os
from collections import OrderedDict
from fiona.transform import transform_geom

def get_data_path(shp_path):
    return os.path.join(shp_path)


def getAdminTypeCode(adminType):
    if adminType == 'area council': return 'ac'
    if adminType == 'atoll': return 'a'
    if adminType == 'census block': return 'blk'
    if adminType == 'census district': return 'cd'
    if adminType == 'constituency': return 'c'
    if adminType == 'division': return 'dv'
    if adminType == 'district': return 'ds'
    if adminType == 'enumeration area': return 'ea'
    if adminType == 'group of islands': return 'g'
    if adminType == 'hamlet': return 'h'
    if adminType == 'island': return 'i'
    if adminType == 'local level government areas': return 'llga'
    if adminType == 'municipality': return 'm'
    if adminType == 'province': return 'p'
    if adminType == 'state': return 's'
    if adminType == 'tikina': return 't'
    if adminType == 'village': return 'v'
    if adminType == 'ward': return 'w'
    return None
    # if adminType == 'localities': return 'l' # in Fiji as points


def getIdField(admin_level_info, available_fields):
    admin_type_code = getAdminTypeCode(admin_level_info['localName'].lower())
    for field in available_fields:
       if field == f"{admin_type_code}id": return f"{admin_type_code}id"
       if field == f"{admin_type_code}_id": return f"{admin_type_code}_id"
       if field == f"{admin_type_code.upper()}ID": return f"{admin_type_code.upper()}ID"

def findNameField(record, admin_level_info, available_fields):
    admin_type_code = getAdminTypeCode(admin_level_info['localName'].lower())
    for field in available_fields:
        if field == f"{admin_type_code}name": return f"{admin_type_code}name"
        if field == f"{admin_type_code}_name": return f"{admin_type_code}_name"
        if field == f"{admin_type_code.upper()}Name": return f"{admin_type_code.upper()}Name"
        if field == f"{admin_type_code.upper()}_Name": return f"{admin_type_code.upper()}_Name"


def record_converter(record, desired_output, admin_level_info, country_info, available_fields, src_crs):
    name_field = findNameField(record, admin_level_info, available_fields)
    id_field = getIdField(admin_level_info, available_fields)
    feature_name = None
    if name_field != None:
        feature_name = record['properties'][name_field]
        if feature_name.isupper() or feature_name.islower():
            feature_name = feature_name.title()
    else: 
        print(f"Could not find name field: {country_info['countryIsoAlpha3Code']}, {admin_level_info['localName']}")
    
    return {
        'geometry': transform_geom(src_crs, "EPSG:3349", record['geometry']),
        'properties': OrderedDict([
            (f"{desired_output['shortName']}_NAME", feature_name),
            (f"{desired_output['shortName']}_CODE", f"{country_info['countryIsoAlpha3Code']}-{record['properties'][id_field]}"),
            ('CNTRY_ISO3', country_info['countryIsoAlpha3Code']),
            ('LC_AD_TYPE', admin_level_info['localName']),
            ('SRC_DS', 'popgis')
        ])
    }
