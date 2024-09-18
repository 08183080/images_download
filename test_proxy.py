import requests

print(requests.get('http://icanhazip.com', timeout=5, proxies={'http':{}, 'https': {}}).text.strip())
