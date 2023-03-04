import requests
import re
import json
from bs4 import BeautifulSoup
from os.path import dirname, abspath
from headers_frenkee_cz import headers, query

cwd_path = dirname(abspath(__file__))


def get_vin(path: str):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
    for i, line in enumerate(vin_code_list):
        vin_code_list[i] = line.strip()
    return vin_code_list


def get_car_info(vin):
    url = "https://www.frenkee.cz/cs/pojisteni-aut"
    new_query = query.copy()
    new_query["carInsuranceDetailForm-vin"] = vin
    response = requests.request("GET", url, params=new_query, headers=headers)
    json_text = json.loads(response.text)
    soup_prep = json_text['snippets']['snippet-carInsuranceDetailForm-detailForm']
    soup = BeautifulSoup(soup_prep, "html.parser")
    return soup, json_text


def collect_car_info(soup, json_text):
    # find car brand and model
    if soup.find('li', attrs={'class': 'lead'}) is None:
        return None
    name = soup.find('li', attrs={'class': 'lead'}).text.strip()

    # find VIN code
    vin = soup.find('li', attrs={'class': 'mb-1'}).text.strip()
    vin = re.search('VIN: (.+)', vin)
    vin = vin.group(1) if vin else None
    # find DATE of first registration
    reg = soup.find('ul', attrs={'class': 'ico-list text-default mb-0'}).text.strip()
    reg = re.search('Datum první registrace: ([0-9]{2}\\.[0-9]{2}\\.[0-9]{4})', reg)
    reg = reg.group(1) if reg else None
    car_info_tag = soup.find('ul', attrs={'id': 'carInformations'}).text.strip()
    license_plate = re.search('(Číslo technického průkazu:)([0-9, A-Z]+)', car_info_tag)
    license_plate = license_plate.group(2) if license_plate else None
    manufacturing_date = re.search('(Měsíc a rok výroby:)( [0-9].+[0-9].+[0-9]{4})', car_info_tag)
    manufacturing_date = manufacturing_date.group(2) if manufacturing_date else None
    fuel_type = re.search('(Typ paliva:)([ A-Z]+)', car_info_tag)
    fuel_type = fuel_type.group(2) if fuel_type else None
    engine_volume = re.search('(Objem motoru:)([ 0-9]+)', car_info_tag)
    engine_volume = engine_volume.group(2) if engine_volume else None
    engine_power = re.search('(Výkon motoru:)([ 0-9]+)', car_info_tag)
    engine_power = engine_power.group(2) if engine_power else None
    car_weight = re.search('(Hmotnost:)([ 0-9, A-z]+)', car_info_tag)
    car_weight = car_weight.group(2) if car_weight else None
    seats_num = re.search('(Počet míst:)([ 0-9]+)', car_info_tag)
    seats_num = seats_num.group(2) if seats_num else None

    car_info = {"main_car_info": {
        "car_vin": vin,
        "car_model": name,
        "number_of_seats": seats_num,
        "date_of_first_registration": reg,
        "plate": license_plate,
        "engine_power": engine_power,
        "engine_volume": engine_volume,
        "other_car_info": {
            "manufacturing_date": manufacturing_date,
            "fuel_type": fuel_type,
            "car_weight": car_weight,
        }
    }}

    return car_info


def get_all_data(vin: str):
    soup, json_text = get_car_info(vin)
    car_info = collect_car_info(soup, json_text)

    if car_info:
        json.dump(car_info, open(f"{cwd_path}/parsed_vins/{vin}.json", "w"), indent=4)
        print(f'{vin} PARSED!')
    else:
        with open(f"{cwd_path}/incorrect_vins.txt", "a+") as f:
            f.write(vin + "\n")
        print(f'{vin} BAD VIN!')


if __name__ == '__main__':
    vin_code_list = get_vin(f"{cwd_path}/vin_frenkee_cz.txt")

    for vin in vin_code_list:
        get_all_data(vin)
