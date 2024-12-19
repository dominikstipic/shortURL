import time
import requests

SLEEP_TIME = 1*60
HOST_NAME = "64.226.98.170"
PORT = 82
url = f"http://{HOST_NAME}:{PORT}/ip"

def get_ip():
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify = True)
    if response.status_code != 200:
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'
    data = response.json()
    return data['ip']

while True:
    ip = get_ip()
    print(ip)
    requests.post(url, json=ip)
    time.sleep(SLEEP_TIME)


