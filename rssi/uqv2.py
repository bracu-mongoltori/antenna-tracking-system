import requests

import urllib3

# Disabling warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Login
login_url = "https://192.168.1.8/api/auth"

login_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0', 
'Accept' : 'application/json, text/javascript, */*; q=0.01',
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip, deflate, br, zstd',
'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
'X-Requested-With' : 'XMLHttpRequest',
'Origin' : 'https://192.168.1.5',
'Connection' : 'keep-alive',
'Referer' : 'https://192.168.1.5/',
'Cookie' : 'ok=1',
'Sec-Fetch-Dest' : 'empty',
'Sec-Fetch-Mode' : 'cors', 
'Sec-Fetch-Site' : 'same-origin',
'DNT' : '1',
'Sec-GPC' : '1',
'Priority' : 'u=0'}

auth = { "username": "ubnt", "password": "mt-rover_123" }

login_response = requests.post(login_url, headers = login_headers, data = auth, verify = False)

cred = login_response.headers['Set-Cookie'].split(';')[0]

print(cred)

# Data

data_url = "https://192.168.1.8/signal.cgi"

data_headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip, deflate, br, zstd',
'Connection' : 'keep-alive',
'Cookie' : f'ok=1; {cred}',
'Upgrade-Insecure-Requests' : '1',
'Sec-Fetch-Dest' : 'document',
'Sec-Fetch-Mode' : 'navigate',
'Sec-Fetch-Site' : 'none',
'Sec-Fetch-User' : '?1',
'DNT' : '1',
'Sec-GPC' : '1',
'Priority' : 'u=0, i'}

while True:
    data_response = requests.get(data_url, headers = data_headers, verify = False)

    print(data_response.text)

    with open("data.json", "a") as file:
        file.write(data_response.text + "\n")
        file.close()
