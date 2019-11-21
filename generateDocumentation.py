import os, shutil, fiona
from pytablewriter import MarkdownTableWriter, HtmlTableWriter
import pandas as pd
import json

import config

json_file = open('compiledDatasets/regionMapping.json')
region_mapping_data = json.load(json_file)['regionMapping']
output_root = "documentation"
data_root = "compiledDatasets"

if not os.path.exists(output_root):
    os.mkdir(output_root)


main_doco = open(os.path.join(output_root, 'README.md'), 'w')

for desired_output in config.desired_outputs:

    main_doco.write(f"## {desired_output['friendlyName']} \n")
    out_dir = os.path.join(output_root, desired_output["outputName"])
    
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    writer = MarkdownTableWriter()
    htmlWrite = HtmlTableWriter()

    writer.table_name = desired_output['friendlyName']
    writer.headers = ["ISO3 Code", "Country", "Boundary type"]
    writer.value_matrix = []

    for country in config.countries:
        if desired_output["countryConfigKey"] in country:
            admin_level_info = country[desired_output["countryConfigKey"]]
            writer.value_matrix.append([country['countryIsoAlpha3Code'], country['countryName'], admin_level_info['localName']])
        else:
            writer.value_matrix.append([country['countryIsoAlpha3Code'], country['countryName'], 'N/A'])

    writer.dump(os.path.join(out_dir, "README.md"))

    htmlWrite.from_tabledata(writer.tabledata)
    htmlWrite.dump(os.path.join(out_dir, "README.html"))

    writer2 = MarkdownTableWriter()
    writer2.table_name = f"{desired_output['friendlyName']} Values"
    writer2.headers = [
        f"{desired_output['shortName']}_NAME",
        f"{desired_output['shortName']}_CODE",
        'ISO3 Code',
        'Local Boundary Name',
        'Source Geometry Dataset'
    ]
    writer2.value_matrix = []

    source = fiona.open(os.path.join(data_root, desired_output["outputName"],  f"{desired_output['outputName']}.shp"))
    available_source_fields = source.schema['properties'].keys()

    for f in source:
        row_data = []
        for field in available_source_fields:
            row_data.append(f['properties'][field])
        writer2.value_matrix.append(row_data)

    writer2.dump(os.path.join(out_dir, "Values.md"))
    
    df = pd.DataFrame(writer2.value_matrix)
    df.columns = writer2.headers
    df = df.drop(columns=['Source Geometry Dataset', 'ISO3 Code'])
    df['SampleValues'] = ""
    df.to_csv(os.path.join(output_root, desired_output["outputName"], "sample.csv"), index=False)


    aliasWriter = MarkdownTableWriter()
    aliasWriter.headers = ['Available Aliases']
    aliasWriter.value_matrix = []
    for alias in region_mapping_data[desired_output["shortName"]]['aliases']:
        aliasWriter.value_matrix.append([alias])
    main_doco.write(aliasWriter.dumps())

main_doco.close()
