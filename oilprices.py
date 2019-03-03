import requests
from bs4 import BeautifulSoup

def curOilPrice():
    response = requests.get('http://rockinghamoil.com/')
    bs = BeautifulSoup(response.text, features='html.parser')
    tag = bs.find('span', class_='customdailyprice')
    pricetxt = tag.text
    price = float(pricetxt.split('$')[1])
    return price