import requests
import json
from os.path import dirname, abspath
from headers_srovnator import headers

cwd_path = dirname(abspath(__file__))


def get_vin(path: str):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
    for i, line in enumerate(vin_code_list):
        vin_code_list[i] = line.strip()

    return vin_code_list


def get_car_info(vin):
    url = f"https://inovis.renomia.cz/car-valuation/get-info/{vin}"

    response = requests.request("GET", url, headers=headers)

    json_text = json.loads(response.text.strip())

    return json_text
#W0L0XCE7594242088


def collect_car_info(json_text):
    if not json_text.get('carInfo'):
        return None
    new_json = json_text['carInfo']
    car_info = {
        "main_car_info": {
            "car_vin": new_json['vin'],
            "car_brand": new_json['manufacturer'],
            "car_model": new_json['model2'] or new_json['model'],
            "number_of_seats": new_json['sittingPlaces'],
            "date_of_first_registration": new_json.get('firstTimeRegistration'),
            "engine_power": new_json['power'],
            "engine_volume": new_json['capacity'],
            "fuelConsumption": new_json['fuelConsumption'],
        },
        "other_car_info": {"fuel_type": new_json['fuelType'],
                           "car_weight": new_json['totalWeight'],
                           "official_note": new_json.get('officialNote'),
                           }
    }

    return car_info


def get_all_data(vin: str):
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
    vin_code_list = get_vin(f"{cwd_path}/vin_srovnator_cz.txt")

    for vin in vin_code_list:
        get_all_data(vin)
