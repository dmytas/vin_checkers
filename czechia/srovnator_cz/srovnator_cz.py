import requests
import json
from headers_srovnator import headers


def get_car_info(vin):
    url = f"https://inovis.renomia.cz/car-valuation/get-info/{vin}"

    response = requests.request("GET", url, headers=headers)

    json_text = json.loads(response.text)

    return json_text


if __name__ == "__main__":
    print(get_car_info("W0L0XCE7594242088"))
