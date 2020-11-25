import requests
import re
from bs4 import BeautifulSoup

def curOilPrice():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get('https://rockinghamoil.com',headers=headers)
    bs = BeautifulSoup(response.text, features='html.parser')
    tag = bs.find('div', class_='et_pb_text_inner')
    pricetxt = tag.next_element.text
    price = re.findall('(?!\$)[\d]*\.[\d]*', pricetxt)
    price = float(price[0])
    return price