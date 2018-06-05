import os
import json
import decimal

TESTS_DIRPATH = os.path.abspath(os.path.dirname(__file__))
ARQS_DIRPATH = os.path.join(TESTS_DIRPATH, 'data')


def get_data_from_file():
    file = open(os.path.join(ARQS_DIRPATH, 'cnabData.json'))
    file_string = file.read()
    json_data = json.loads(file_string)
    json_data = convert_to_decimal(json_data)
    file.close()
    return json_data


def convert_to_decimal(data):
    for record in data.values():
        for key, value in record.items():
            if key.startswith("valor"):
                record[key] = decimal.Decimal(value)
    return data
