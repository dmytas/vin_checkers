import json
import requests
from netfinancie_sk_haeders import headers, body
from os.path import dirname, abspath

cwd_path = dirname(abspath(__file__))


def get_vin(path: str):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
    for i, line in enumerate(vin_code_list):
        vin_code_list[i] = line.strip()

    return vin_code_list


def get_car_info(vin):
    url = "https://www.netfinancie.sk/api-xform/"
    new_body = body.copy()
    new_body["search"] = vin
    response = requests.request("POST", url, headers=headers, data=new_body)
    json_text = json.loads(response.text)
    return json_text


def collect_car_info(json_text):
    if not json_text.get('newformdata'):
        return None
    new_json = json_text['newformdata']
    car_info = {
        "main_car_data": {
            "car_vin": new_json['vozidlo_vin'],
            "car_model": new_json['vozidlo_model'],
            "number_of_seats": new_json['vozidlo_pocet_miest_na_sedenie'],
            "date_of_first_registration": new_json['vozidlo_datum_prvej_evidencie'],
            "plate": new_json['vozidlo_ecv'],
            "engine_power": new_json['vozidlo_objem_valcov'],
            "engine_volume": new_json['vozidlo_vykon_motora'],
            "other_car_data": {
                "fuel_type": new_json['vozidlo_druh_paliva'],
                "car_weight": new_json['vozidlo_celkova_hmotnost'],
                "some_car_data": json_text['data'],
                "gear_box_type": new_json['vozidlo_typ_prevodovky'],
                "number_of_gears": new_json['vozidlo_typ_prevodovky'],

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
    vin_code_list = get_vin(f"{cwd_path}/vin_netfinancie.txt")

    for vin in vin_code_list:
        get_all_data(vin)
