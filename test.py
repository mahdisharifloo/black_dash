import requests
import json

url = "http://0.0.0.0:10015/get_news"

querystring = {"record_count":"100"}

payload = ""
headers = {"accept": "application/json"}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
data = json.loads(response.text)
t1 = data[:50]
t2 = data[50:]
print(data)