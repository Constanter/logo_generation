import requests

IP = requests.get('https://api.ipify.org').text
print(IP)