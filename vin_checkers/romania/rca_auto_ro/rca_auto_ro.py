import requests
import json
from headers_rca_auto_ro import headers
from os.path import dirname, abspath

cwd_path = dirname(abspath(__file__))


def get_vin(path: str):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
    for i, line in enumerate(vin_code_list):
        vin_code_list[i] = line.strip()

    return vin_code_list


def get_car_info(vin):
    url = f"https://www.rca-auto.ro/asigurare-rca/import-drpciv?vin={vin}"
    response = requests.request("GET", url, headers=headers)
    json_text = json.loads(response.text)
    return json_text


def collect_car_info(json_text):
    if json_text:
        car_info = {"main_car_info": {
            "car_vin": json_text.get('serie_sasiu'),
            "car_model": json_text.get('model'),
            "car_brand": json_text.get('marca'),
            "year_of_manufacturing": json_text.get('an_fabricatie'),
            "engine_power": json_text.get('cilindree'),
            "engine_volume": json_text.get('putere'),
            "number_of_seats": json_text.get('locuri'),
            "other_car_info": {
                "fuel_type": json_text.get('carburant'),
                "car_weight": json_text.get('masa_maxima'),

            }
        }}
        return car_info
    else:
        return None


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
    vin_code_list = get_vin(f"{cwd_path}/vin_rca_auto_ro.txt")
    for vin in vin_code_list:
        get_all_data(vin)
