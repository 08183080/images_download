import requests

proxies = {'http':{}, 'https': {}}

print(requests.get('http://icanhazip.com', timeout=5).text.strip())  # proxy ip

print(requests.get('http://icanhazip.com', timeout=5, proxies=None).text.strip()) # proxy ip

print(requests.get('http://icanhazip.com', timeout=5, proxies={}).text.strip()) # proxy ip

print(requests.get('http://icanhazip.com', timeout=5, proxies=proxies).text.strip()) # original ip