import requests
import json
import re
from bs4 import BeautifulSoup
from os.path import dirname, abspath
from headers_autopojisteni_koop_cz import headers

cwd_path = dirname(abspath(__file__))


def get_vin(path: str):
    with open(path, "r") as txt_vin:
        vin_code_list = txt_vin.readlines()
    for i, line in enumerate(vin_code_list):
        vin_code_list[i] = line.strip()

    return vin_code_list


def get_car_info(vin):
    url = f"https://autopojisteni.koop.cz/autopojisteni/zakladni-udaje/basicDataSubmit?frm.birthEnt.variant=bn&frm" \
          f".birthInd.number=7401233642&frm.birthInd.variant=bn&frm.callcentrum.phone=%2B420789412689&frm.carType.car" \
          f"=A&frm.carType.other=F&frm.carType.truck=C1&frm.carTypeCategory=car&frm.carValue=0&frm.customerType" \
          f"=INDIVIDUAL&frm.insuranceType=POV&frm.licensePlateOrVin=" \
          f"{vin}&frm.name=Radek&frm.operator=true&frm.operatorBirthEnt.variant=bn&frm.operatorBirthInd.variant=bn" \
          f"&frm.operatorType=INDIVIDUAL&frm.owner=true&frm.ownerBirthEnt.variant=bn&frm.ownerBirthInd.variant=bn&frm" \
          f".ownerType=INDIVIDUAL&frm.slug=pojisteni&frm.slug=pojisteni-vozidel&frm.slug=pojisteni-automobilu&frm" \
          f".slug=povinne-ruceni&frm.surname=Stam&frm.zipCode=10200 "
    response = requests.request("GET", url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def collect_car_info(soup):
    div = soup.find('div', attrs={"class": "typeahead"})
    all_car_data = re.search('data-typeahead-url=(.+)', str(div)).group(0)
    vin_code = re.search('(licensePlateOrVin=)([0-9, A-Z]{17})', all_car_data)
    vin_code = vin_code.group(2) if vin_code else None
    car_brand = re.search('(carBrand=)([A-Z]+)', all_car_data)
    car_brand = car_brand.group(2) if car_brand else None
    car_model = re.search('(carModel=)([A-Z]+)', all_car_data)
    car_model = car_model.group(2) if car_brand else None
    fuel_type = re.search('(fuel=)([A-Z]+)', all_car_data)
    fuel_type = fuel_type.group(2) if fuel_type else None
    seats_num = re.search('(seats=)([0-9])', all_car_data)
    seats_num = seats_num.group(2) if seats_num else None
    license_plate = re.search('(licensePlate=)([0-9, A-Z]+)', all_car_data)
    license_plate = license_plate.group(2) if license_plate else None
    engine_volume = re.search('(engineVolume=)([0-9]+)', all_car_data)
    engine_volume = engine_volume.group(2) if engine_volume else None
    car_weight = re.search('(weight=)([0-9]+)', all_car_data)
    car_weight = car_weight.group(2) if car_weight else None
    engine_power = re.search('(enginePower=)([0-9]+)', all_car_data)
    engine_power = engine_power.group(2) if engine_power else None
    technical_certificate = re.search('(technicalCertificateNo=)([0-9, A-Z]+)', all_car_data)
    technical_certificate = technical_certificate.group(2) if technical_certificate else None
    first_license = re.search('(firstLicensed=)([0-9].+[0-9].+[0-9]{4})', all_car_data)
    first_license = first_license.group(2) if first_license else None
    if car_model:
        car_info = {
            "car_vin": vin_code,
            "car_brand": car_brand,
            "car_model": car_model,
            "fuel_type": fuel_type,
            "number_of_seats": seats_num,
            "plate": license_plate,
            "engine_volume": engine_volume,
            "engine_power": engine_power,
            "car_weight": car_weight,
            "technical_certificate": technical_certificate,
            "first_license": first_license

        }
        return car_info
    else:
        return None


def get_all_data(vin):
    soup = get_car_info(vin)
    car_info = collect_car_info(soup)
    if car_info:
        json.dump(car_info, open(f"{cwd_path}/parsed_vins/{vin}.json", "w"), indent=4)
        print(f'{vin} PARSED!')
    else:
        with open(f"{cwd_path}/incorrect_vins.txt", "a+") as f:
            f.write(vin + "\n")
        print(f'{vin} BAD VIN!')


if __name__ == "__main__":
    vin_code_list = get_vin(f"{cwd_path}/vin_autopojisteni_koop_cz.txt")
    for vin in vin_code_list:
        get_all_data(vin)
