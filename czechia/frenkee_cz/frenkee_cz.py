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

    car_data = {
        'car_model': name,
        'vin_code': vin,
        'date_of_first_registration': reg
    }

    # find other car info
    car_info = {}
    car_info.update(car_data)
    car_info_tag = soup.find('ul', attrs={'id': 'carInformations'})
    for tag in car_info_tag.find_all('li'):
        tag_string = tag.text.strip()
        key_value = re.search('(.+): (.+)', tag_string)
        if key_value:
            car_info[key_value.group(1)] = key_value.group(2)

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