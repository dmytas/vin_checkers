import json
from os.path import dirname, abspath

import requests

from headers_allianz_be import headers

cwd_path = dirname(abspath(__file__))


def get_vin(path):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
        for i, line in enumerate(vin_code_list):
            vin_code_list[i] = line.strip()
        return vin_code_list


def get_car_info(vin):
    url = f"https://apps.allianz.be/FastQuoteRest/api/products/car/vin/{vin}"
    response = requests.request("GET", url, headers=headers)
    json_text = json.loads(response.text)
    return json_text


def collect_car_info(json_text):
    if not json_text.get("root"):
        return None
    new_json = json_text["root"]["body"]
    car_data = new_json.get("technical")
    car_reg = new_json.get("registration")
    car_manufactured = new_json.get("labels")
    car_manufactured = car_manufactured if car_manufactured else {}
    car_info = {
        "main_car_info":
            {"car_vin": car_reg.get("vin"),
             "date_of_first_registration": car_reg.get("registrationFirst"),
             "date_of_last_registration": car_reg.get("registrationLast"),
             "registration_status": car_reg.get("registrationStatus"),
             "car_brand": car_manufactured.get("manufacturer"),
             "car_model": car_manufactured.get("model"),
             "car_model_type": car_manufactured.get("type"),
             "car_color": car_data.get("color"),
             "number_of_seats": car_data.get("seats"),
             "engine_power": car_data.get("kw"),
             "engine_volume": car_data.get("cc"),
             "co2": car_data.get("co2"),
             

             "other_car_info": {
                 "car_weight": car_data.get("massInRunning"),
                 "gear_box_type": car_data.get("transmissionType"),
                 "number_of_gears": car_data.get("gears"),
                 "fraud_detection": new_json.get("fraudDetection"),
                 "damage_cost": new_json.get("damageCosts"),
                 "car_equipment": new_json.get("safety"),

             }
             }
    }
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
    vin_code_list = get_vin(f"{cwd_path}/vin_allianz_be.txt")

    for vin in vin_code_list:
        get_all_data(vin)
