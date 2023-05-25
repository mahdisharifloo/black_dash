import requests
import json 


url = "http://192.168.18.170:10015/get_statistics"

payload = {}
headers = {
'accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

resp = json.loads(response.text)