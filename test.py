# https://coinmarketcap.com/currencies/bnb/markets/

from os import link
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import json
import time
import json_parse2

# Base of other URL's
uri_base = 'https://coinmarketcap.com'
# List of birges to parse
birges = ['bybit', 'binance', 'kucoin', 'huobi', 'coinbase exchange', 'ftx', 'okx', 'kraken',
          'phemex', 'gate.io', 'lbank', 'crypto.com exchange', 'aex', 'mexc', 'whitebit']

def main():
    start_time = time.time()

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

    browser = webdriver.Chrome('/Users/gamch1k/Documents/chromedriver', options=options)

    print('PARSING COINS')

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

    print('GOT ALL COINS')


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
            f.write('')
        with open(f'jsons/raw/{f_name}.json', 'w') as f:
            f.write('')
        with open(f'jsons/raw/{f_name}.json', 'w') as f:
            json.dump(data, f, indent=4)

    browser.quit()
    json_parse2.main()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    while True:
        main()
        time.sleep(600)
