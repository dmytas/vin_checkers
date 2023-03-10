import requests
import json
from os.path import dirname, abspath
from headers_asigurari_ro import headers, body

cwd_path = dirname(abspath(__file__))


def get_vin(path: str):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
    for i, line in enumerate(vin_code_list):
        vin_code_list[i] = line.strip()

    return vin_code_list


def get_car_info(vin):
    url = "https://www.asigurari.ro/api/broker/vehicle/lookup"
    new_body = body.copy()
    new_body["chassisSerial"] = vin
    response = requests.request("POST", url, headers=headers, json=new_body)
    if response.status_code == 500:
        json_text = []
    else:
        json_text = json.loads(response.text)

    return json_text


def collect_car_info(json_text):
    if not json_text:
        return None
    car_info = {
        "main_car_info": {
            "car_vin": json_text.get('vehicle-chassis_serial'),
            "car_model": json_text.get('vehicle-model'),
            "car_color": json_text.get('vehicle-color'),
            "car_brand": json_text.get('vehicle-make'),
            "number_of_seats": json_text.get('vehicle-seats'),
            "year_of_manufacturing": json_text.get('vehicle-manuf_yea'),
            "engine_power": json_text.get('vehicle-engine_size'),
            "engine_volume": json_text.get('vehicle-engine_power'),
            "other_car_info": {
                "fuel_type": json_text.get('vehicle-fuel_type'),
                "car_weight": json_text.get('vehicle-max_weight'),
            }

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
    vin_code_list = get_vin(f"{cwd_path}/vin_asigurari.txt")

    for vin in vin_code_list:
        get_all_data(vin)

