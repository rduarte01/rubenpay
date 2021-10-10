import json
import requests
from datetime import datetime, timedelta
from rest_framework.response import Response
import http.client
import datetime
import pprint

from config import *

HOST = "staging.adamspay.com"
APIKEY = settings["APIKEY"]


def api_deuda_list():

    url = "https://"+ HOST + "/api/v1/debts"

    payload={}
    headers = {
    'apikey': APIKEY,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response.json()

def api_deuda(idDoc):

    url = "https://"+ HOST + "/api/v1/debts/"+str(idDoc)

    payload={}
    headers = {
    'apikey': APIKEY,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.json()["debt"])
    docId = response.json()["debt"]["docId"]
    label = response.json()["debt"]["label"]
    payUrl = response.json()["debt"]["payUrl"]
    value = response.json()["debt"]["amount"]["value"]
    start = response.json()["debt"]["validPeriod"]["start"]
    end = response.json()["debt"]["validPeriod"]["end"]
    return docId,label,payUrl,value,start,end
    

def api_deuda_new(idDeuda,f1,f2,valor,desc):
    from datetime import datetime
    siExiste = "update"
    apiKey = APIKEY
    host = HOST
    path = "/api/v1/debts"

    # Crear modelo de la deuda
    deuda = {
        "docId": idDeuda,
        "amount": {"currency": "PYG","value": valor},
        "label":desc,
        "validPeriod":{
        #"start":inicio_validez.strftime("%Y-%m-%dT%H:%M:%S"),
        #"end":fin_validez.strftime("%Y-%m-%dT%H:%M:%S")
        "start":f1,
        "end":f2
        }  
    }
    
    # El post debe llevar la deuda en la propiedad "debt"
    post = {"debt":deuda}
    
    # Crear JSON
    payload = json.JSONEncoder().encode(post).encode("utf-8")
    
    headers = {"apikey": apiKey, "Content-Type": "application/json", "x-if-exists": siExiste}
    conn = http.client.HTTPSConnection(host)
    conn.request("POST", path , payload, headers)
    
    data = conn.getresponse().read().decode("utf-8")
    response = json.JSONDecoder().decode(data)
    
    # Datos retornan en la propiedad "debt"
    
    pp = pprint.PrettyPrinter(indent=2)
    if "debt" in response:
        debt=response["debt"]
        print("Deuda creada exitosamente")
        print("URL=" + debt["payUrl"])
    else:
        print("# Error")
        if "meta" in response:
            pp.pprint(response["meta"])