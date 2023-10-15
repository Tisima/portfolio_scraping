from time import sleep

from bs4 import BeautifulSoup
import requests
import pandas as pd


with open('company_list.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')
a_tags = soup.select('span.bl_card2_ttl_text > a')
print('取得した企業数:', len(a_tags))
d_list = []
for i, a_tag in enumerate(a_tags):
    url = 'https://atsumaru.jp' + a_tag.get('href')
    r = requests.get(url)
    r.raise_for_status()

    sleep(3)

    page_soup = BeautifulSoup(r.content, 'lxml')

    company_name = page_soup.select_one(
        'span.bl_card2_ttl_text').text.replace('\u3000', '')
    if page_soup.select_one(
            'td:-soup-contains("地図はこちら") > p:first-of-type') != None:
        address = page_soup.select_one(
            'td:-soup-contains("地図はこちら") > p:first-of-type').text.replace('\u3000', '')
    else:
        address = 'なし'
    if page_soup.select_one(
            'div.telNo > p > strong > a') != None:
        tel = page_soup.select_one(
            'div.telNo > p > strong > a').text.replace('\u3000', '')
    else:
        tel = 'なし'
    d_list.append({
        '会社名': company_name,
        '住所': address,
        '電話番号': tel
    })

    print('='*30, i, '='*30)
    print(d_list[-1])
    if i == 100:
        break

df = pd.DataFrame(d_list)
df.to_csv('company_list.csv', index=None, encoding='utf-8-sig')
