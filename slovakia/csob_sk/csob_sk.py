import requests
import json
from csob_sk_headers import headers
from os.path import dirname, abspath

cwd_path = dirname(abspath(__file__))


def get_vin(path):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
        for i, line in enumerate(vin_code_list):
            vin_code_list[i] = line.strip()
        return vin_code_list


def get_car_info(vin):
    url = f"https://poistenie.csobpoistovna.sk/pzp/api/vehicle/vin/{vin}"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 500:
        return None
    else:
        json_text = json.loads(response.text)
    return json_text


def collect_car_info(json_text):
    if json_text is None:
        return None
    elif json_text['manufacturer'] is None:
        return None
    car_info = {
        "main_car_info": {
            "car_model": json_text.get('model'),
            "car_brand": json_text.get('manufactured'),
            "engine_power": json_text.get('enginePower'),
            "engine_volume": json_text.get('engineCapacity'),
            "plate": json_text.get('ecv'),
            "policyholder": json_text.get('tp'),

            "other_car_info": {
                "car_weight": json_text.get('totalWeight'),

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
    vin_code_list = get_vin(f"{cwd_path}/vin_csob.txt")

    for vin in vin_code_list:
        get_all_data(vin)

