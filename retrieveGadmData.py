import requests, zipfile, io, os

import config

src_data_path = "srcDatasets/gadm"
if not os.path.exists(src_data_path):
    os.mkdir(src_data_path)

for country in config.countries:
    country_dir = os.path.join(src_data_path, country['countryIsoAlpha3Code'])
    if not os.path.exists(country_dir):
        os.mkdir(country_dir)
    else:
        print(f"Already have GADM data for {country['countryName']}")
        continue

    r = requests.get(f"https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_{country['countryIsoAlpha3Code']}_shp.zip")
    if r.status_code == 200:
        with open(os.path.join(country_dir, f"gadm36_{country['countryIsoAlpha3Code']}_shp.zip"), "wb") as f:
            f.write(r.content)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(country_dir)
    else: 
        print(f"No GADM data for {country['countryName']}")
