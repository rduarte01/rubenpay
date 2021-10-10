import json
import requests
from datetime import datetime, timedelta
from rest_framework.response import Response
from config import *

HOST = "https://staging.adamspay.com"
APIKEY = settings["APIKEY"]


def api_deuda_list():

    url = HOST + "/api/v1/debts"

    payload={}
    headers = {
    'apikey': APIKEY,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response.json()
