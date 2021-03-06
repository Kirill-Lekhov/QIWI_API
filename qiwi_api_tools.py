import json
import time
import requests
import math


def run_the_query(headers, url):
    try:
        response = requests.get(url, headers=headers)
        if response:
            return response.json()

        return False
    except:
        return False


def found_address(ip):
    try:
        response = requests.get('http://freegeoip.net/json/{}'.format(ip))
        if response:
            json_response = response.json()
            return json_response["city"]
        else:
            return False
    except:
        return False


def write_file(headers, url, file_name):
    try:
        with open(file_name, mode='wb') as f:
            response = requests.get(url, headers=headers)

            if not response:
                return False

            f.write(response.content)

        return True
    except:
        return False


def found_id(number):
    headers = {"Accept": "application/json",
               "Content-Type": "application/x-www-form-urlencoded"}

    user_number = correct_number(number)

    if not user_number:
        return False

    data = {"phone": user_number}
    try:
        request = requests.post("https://qiwi.com/mobile/detect.action", data=data, headers=headers)
        if request:
            answer = request.json()
            if answer["code"]["value"] != '0':
                return False
            return answer["message"]
        else:
            return False
    except:
        return False


def correct_number(number):
    if len(number) < 11:
        return False

    if number[0] != "8" and number[0] != "7" and number[:2] != "+7":
        return False

    if number[0] == "8":
        number = "7" + number[1:]

    new_number = ""

    for i in number:
        if i.isdigit():
            new_number += i

    return "+" + new_number


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)

    return distance
