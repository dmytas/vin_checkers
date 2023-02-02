import json
import requests
from typing import AnyStr, Dict
from os.path import dirname, abspath
from netfinancie_sk_haeders import headers, body

cwd_path = dirname(abspath(__file__))


def get_vins(path: str):
    vins_file = open(cwd_path, 'r+', encoding='utf-8')
    vin_code_list = vins_file.readlines()
    vins_file.close()

    for i, line in enumerate(vin_code_list):
        vin_code_list[i] = line.strip()

    return vin_code_list


def get_car_info(vin: AnyStr):
    url = "https://www.netfinancie.sk/api-xform/"
    new_body = body.copy()
    new_body["search"] = vin
    response = requests.request("POST", url, headers=headers, data=new_body)
    json_text = json.loads(response.text)
    return json_text


def collect_car_info(json_text: Dict):
    if not json_text.get('newformdata'):
        return None
    car_info = {
        "car_info": json_text['newformdata'],
        "car_data": json_text['data']
    }
    return car_info


def get_data(vin: AnyStr):
    json_text = get_car_info(vin)
    car_info = collect_car_info(json_text)
    if car_info:
        json.dump({vin: car_info}, open(f"{cwd_path}/{vin}.json", "w"), indent=4)
        print(f'{vin} - PARSED!')
    else:
        bad_vins = open(f"{cwd_path}/incorrect_vins.txt", "a+")
        bad_vins.write(vin + "\n")
        print(f'{vin} - BAD!')
        bad_vins.close()

    # return res


if __name__ == "__main__":
    vin_code_list = get_vins(f'{cwd_path}/vins.txt')

    for vin in vin_code_list:
        get_data(vin)
