import requests


def get_ip_address():
    public_ip = None
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except requests.RequestException as e:
        print(f"Error retrieving public IP address: {e}")
    return public_ip