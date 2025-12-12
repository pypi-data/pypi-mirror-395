import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://10.247.224.39/piwebapi"

def get_webid_by_path(tag):
    url = f"{BASE_URL}/points"
    r = requests.get(url, params={"path": f"\\\\pims\\{tag}"}, verify=False)
    return r.json()["WebId"]


def escrever_valor(tag, valor, timestamp):
    webid = get_webid_by_path(tag)
    payload = [
        {"Timestamp": timestamp, "Value": valor}
    ]

    url = f"{BASE_URL}/streams/{webid}/recorded"
    r = requests.post(url, json=payload, verify=False)
    r.raise_for_status()
    print("Valor escrito com sucesso!")