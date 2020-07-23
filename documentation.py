import json
from pathlib import Path

import yaml

from utils import build_url, get_url, write_to_file, format_output, normalize


def document():
    # load data from yaml file
    data = yaml.safe_load(Path('data.yaml').read_text())

    # set some variables for us to use
    output_dir = "output"
    device = data.get('controller')
    endpoint_data = data.get('endpoints')
    port = data.get('api_port')
    host = device.get('host')
    user = device.get('username')
    pw = device.get('password')

    params = {"with-defaults": "report-all"}

    # get the data for each endpoint defined in the data
    # for example: vlans: Cisco-IOS-XE-vlan-oper:vlans/vlan
    # in which case, ep_name = 'vlans' and ep_value = 'Cisco-IOS-XE-vlan-oper:vlans/vlan'
    combined_data = {}
    for ep_name, ep_value in endpoint_data.items():
        url = build_url(host, ep_value, port=port)

        print(f'retrieving data for: {ep_name}')
        json_data = get_url(url, auth=(user, pw), params=params)

        combined_data.update(json_data)

    outputfile_stem = "combined_output"

    print(f'saving data to file: {outputfile_stem}.json')
    input_string = json.dumps(combined_data, indent=2)
    formatted_output = format_output(input_string)
    normalize(formatted_output)
    write_to_file(outputfile_stem, formatted_output, output_dir=output_dir)



if __name__ == '__main__':
    document()
