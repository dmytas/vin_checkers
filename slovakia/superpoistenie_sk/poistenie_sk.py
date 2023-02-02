import requests
import json

from headers_poistenie import headers


def get_car_info(vin):
    url = f"https://poistenie.csobpoistovna.sk/pzp/api/vehicle/vin/{vin}"
    response = requests.request("GET", url, headers=headers)
    json_text = json.loads(response.text)
    return json_text


if __name__ == "__name__":
    print(get_car_info("WF0UXXGAJU3D64260"))
