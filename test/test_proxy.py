import requests

proxies = {'http':{}, 'https': {}}
# proxies={'http':'127.0.0.1:7890', 'https': '//127.0.0.1:7890'}

print(requests.get('http://icanhazip.com', timeout=5).text.strip())  # proxy ip

print(requests.get('http://icanhazip.com', timeout=5, proxies=None).text.strip()) # proxy ip

print(requests.get('http://icanhazip.com', timeout=5, proxies={}).text.strip()) # proxy ip

print(requests.get('http://icanhazip.com', timeout=5, proxies=proxies).text.strip()) # original ip