# https://coinmarketcap.com/currencies/bnb/markets/

from os import link
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time
import json_parse2
from os import listdir
from os.path import isfile, join
from os import remove
import threading

# Base of other URL's
uri_base = 'https://coinmarketcap.com'
# List of birges to parse
birges = ['bybit', 'binance', 'exmo', 'huobi', 'coinbase exchange', 'ftx', 'okx', 'kraken',
          'phemex', 'gate.io', 'lbank', 'crypto.com', 'crypto.com exchange', 'aex', 'mexc', 'whitebit']

# Doing selenium without UI
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

browser = webdriver.Chrome('./chromedriver1', options=options)

def coins_parse():
    print('PARSING COINS')
    # https://coinmarketcap.com
    browser.get(uri_base)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
    time.sleep(2)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Getting coins links
    tbody = soup.find('tbody')
    soup = BeautifulSoup(str(tbody), 'html.parser')
    tr = soup.findAll('tr')
    tr = tr[5:]

    links_arr = []
    for i in tr:
        links_arr.append(BeautifulSoup(str(i), 'html.parser').find('a')['href'] + 'markets/')
        
        
    browser.get(uri_base + '/?page=2')
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
    time.sleep(2)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Getting coins links
    tbody = soup.find('tbody')
    soup = BeautifulSoup(str(tbody), 'html.parser')
    tr = soup.findAll('tr')

    for i in tr:
        links_arr.append(BeautifulSoup(str(i), 'html.parser').find('a')['href'] + 'markets/')

    print('GOT ALL COINS')
    return links_arr

def birg_parse(links_arr):
    for lnk_name in links_arr:
        browser.get(uri_base + lnk_name)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
        time.sleep(2)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        tbody = soup.find('tbody')

        soup = BeautifulSoup(str(tbody), 'html.parser')
        tr = soup.findAll('tr')

        data = {}

        for i in tr:
                try:
                    j = BeautifulSoup(str(i), 'html.parser')
                    td = j.findAll('td')
                    name = BeautifulSoup(str(td[1]), 'html.parser').text
                    if ('/USDT' in j.text) and (name.lower() in birges):
                        pair = BeautifulSoup(str(td[2]), 'html.parser').text
                        price = BeautifulSoup(str(td[3]), 'html.parser').text
                        data[f'{name}({pair})'] = float(str(price)[1:].replace(',', ''))
                except Exception as e:
                    print('EXCEPTION', str(i), str(e))
                    continue
        
        f_name = lnk_name.replace("/currencies/", "").replace("/markets/", "")
        with open(f'jsons/raw/{f_name}.json', 'a') as f:
            json.dump(data, f, indent=4)
    # browser.quit()
    


if __name__ == '__main__':
    while True:
        start_time = time.time()
        arr = coins_parse()
        
        onlyfiles = [f for f in listdir('./jsons/raw') if isfile(join('./jsons/raw', f))]
        for file_name in onlyfiles:
            remove(f'jsons/raw/{file_name}')
        
        threads = []
        x1 = threading.Thread(target=birg_parse, args=(arr[int(len(arr)/4):], ))
        x2 = threading.Thread(target=birg_parse, args=(arr[int(len(arr)/4):int(len(arr)/2)], ))
        x3 = threading.Thread(target=birg_parse, args=(arr[int(len(arr)/2):int(len(arr)/4)*3], ))
        x4 = threading.Thread(target=birg_parse, args=(arr[:int(len(arr)/4)*3], ))
        
        x1.start()
        threads.append(x1)
        x2.start()
        threads.append(x2)
        x3.start()
        threads.append(x3)
        x4.start()
        threads.append(x4)
        
        for thread in threads:
            thread.join()
        
        print('READY')
        json_parse2.main()
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(300)
