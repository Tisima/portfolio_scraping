from selenium import webdriver
from time import sleep, time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')

driver_path = '/Users/toshihirochishima/Desktop/python/tools/chromedriver'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)

driver.get('https://atsumaru.jp/area/7/list?sagid=all')
sleep(3)

height = driver.execute_script("return document.body.scrollHeight")
new_height = 0

while True:
    print(height)
    driver.execute_script(f'window.scrollTo(0, {height});')
    sleep(5)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if height == new_height:
        break

    height = new_height

sleep(3)

with open('company_list.html', 'w') as f:
    f.write(driver.page_source)

driver.quit()
