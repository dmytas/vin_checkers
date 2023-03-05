import json
import requests
from headers_kupi_laqo_cr import headers
from os.path import dirname, abspath

cwd_path = dirname(abspath(__file__))


def get_vin(path: str):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
    for i, line in enumerate(vin_code_list):
        vin_code_list[i] = line.strip()

    return vin_code_list


def get_car_info(vin):
    url = f"https://api.laqo.hr/webshop/backend/vehicle-api/v2/vehicles?vin={vin}"
    response = requests.request("GET", url, headers=headers)
    json_text = json.loads(response.text)
    return json_text


def collect_car_info(json_text):
    if not json_text.get('type'):
        return None
    car_info = {"main_car_info": {
        "car_vin": json_text.get('vin'),
        "car_model": json_text.get('line'),
        "car_color": json_text.get('color'),
        "car_brand": json_text.get('manufacturer'),
        "car_model_detail": json_text.get('model'),
        "number_of_seats": json_text.get('seats'),
        "year_of_manufacturing": json_text.get('year'),
        "date_of_first_registration": json_text.get('registrationDate'),
        "plate": json_text.get('plateNumber'),
        "engine_power": json_text.get('cc'),
        "engine_volume": json_text.get('kw'),
        "engine_number": json_text.get('engineNumber'),
        "policy_num": json_text.get('policyNumber'),
        "policy_expiration_date": json_text.get('policyExpirationDate'),
        "other_car_info": {
            "fuel_type": json_text.get('fuelType'),
            "car_weight": json_text.get('weight'),
        }
    }}
    return car_info


def get_all_data(vin):
    json_text = get_car_info(vin)
    car_info = collect_car_info(json_text)
    if car_info:
        json.dump(car_info, open(f"{cwd_path}/parsed_vins/{vin}.json", "w"), indent=4)
        print(f'{vin} PARSED!')
    else:
        with open(f"{cwd_path}/incorrect_vins.txt", "a+") as f:
            f.write(vin + "\n")
        print(f'{vin} BAD VIN!')


if __name__ == "__main__":
    vin_code_list = get_vin(f"{cwd_path}/vin_kupi_laqo_cr.txt")
    for vin in vin_code_list:
        get_all_data(vin)
