import requests, zipfile, io, os
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset

import config

def guessAdminLevel(name):
    pos = name.index('adm')
    return name[pos + 3]
    # 'fji_polbnda_adm0_country.zip'

Configuration.create(hdx_site='prod', user_agent='BoundaryRetrieval', hdx_read_only=True)


src_data_path = "srcDatasets/hdx"
if not os.path.exists(src_data_path):
    os.mkdir(src_data_path)

for country in config.countries:
    
    out = Dataset.search_in_hdx(f"{country['countryName']} administrative polygon", limit=1)

    if (len(out) > 0):
        country_dir = os.path.join(src_data_path, country['countryIsoAlpha3Code'])
        if not os.path.exists(country_dir):
            os.mkdir(country_dir)

        resources = Dataset.get_all_resources(out)

        for resource in resources:
            if resource['format'] != 'ZIPPED SHAPEFILE':
                continue

            level = guessAdminLevel(resource['name'])

            r = requests.get(resource['url'])

            if r.status_code == 200:
                with open(os.path.join(country_dir, f"hdx_{country['countryIsoAlpha3Code']}_adminLevel{level}_shp.zip"), "wb") as f:
                    f.write(r.content)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(country_dir)
    else: 
        print(f"No HDX data for {country['countryName']}")
