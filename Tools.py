import requests
from urllib import request, parse
from json import loads


# TODO: rework all


def run_the_query(headers, url) -> dict:
    try:
        req = request.Request(url, headers=headers)
        html = loads(request.urlopen(req).read().decode('utf-8'))

        return html

    except Exception as err:
        print(err)
        return {}


def write_file(headers, url, file_name):
    try:
        req = request.Request(url, headers=headers)

        with open(file_name, mode='wb') as f:
            res = request.urlopen(req).read()
            f.write(res)

        return True

    except Exception as err:
        print(err)
        return False


def found_id(number):
    headers = {"Accept": "application/json",
               "Content-Type": "application/x-www-form-urlencoded"}
    data = parse.urlencode({"phone": "+" + number})

    try:
        request = requests.post("https://qiwi.com/mobile/detect.action", data=data, headers=headers)

        if request:
            answer = request.json()

            if answer["code"]["value"] != '0':
                return False

            return answer["message"]

        else:
            return False

    except Exception as err:
        print(err)
        return False
