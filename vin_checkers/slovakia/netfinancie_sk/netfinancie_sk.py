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
    car_info = {
        "car_info": json_text['newformdata'],
        "car_data": json_text['data']
    }
    return car_info


def get_all_data(path):
    res = {}
    vin_code_list = get_vin(path)

    for vin in vin_code_list:
        json_text = get_car_info(vin)
        car_info = collect_car_info(json_text)
        if car_info:
            res[vin] = car_info
            json.dump({vin: car_info}, open(f"{vin}.json", "w"), indent=4)
        else:
            with open(f"{cwd_path}/incorrect_vins.txt", "a+") as f:
                f.write(vin + "\n")

    return res


print(get_all_data("vin.txt"))
