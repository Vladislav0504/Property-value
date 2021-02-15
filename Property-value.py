from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re

#Считывание html
URL = 'https://www.bn.ru/detail/flats/3600782/' 
resp = urlopen(URL)
html = resp.read().decode('utf8')
soup = BeautifulSoup(html, 'html.parser')

#Адрес
metro = soup.find('span', class_='object__header-metro-name').text
address = soup.find('a', href="#map-yandex").text

#Цена
cost_finding = soup.find_all('head')
cost = ''
for elem in cost_finding:
  text = elem.find('title').text
  match = re.search(r'цена -', text)
  cost = text[match.end() + 1:]

#Таблицы Квартира и Дом
flat_and_house_finding = soup.find_all('div', class_="object__param-column")
flat_list_name = [div.text for div in flat_and_house_finding[0].find_all('div', class_="object__param-item-name")]
flat_list_value = [div.text for div in flat_and_house_finding[0].find_all('div', class_="object__param-item-value")]
house_list_name = [div.text for div in flat_and_house_finding[1].find_all('div', class_="object__param-item-name")]
house_list_value = [div.text for div in flat_and_house_finding[1].find_all('div', class_="object__param-item-value")]
flat = {flat_list_name[i]: flat_list_value[i] for i in range(len(flat_list_name))}
house = {house_list_name[i]: house_list_value[i] for i in range(len(house_list_name))}

#Описание
description = soup.find('div', class_="object__comment")

#Информация
Description = {
'Адрес': ('метро ' + metro, address), 
'Цена': cost,
'Квартира': flat,
'Дом': house,
'Описание': description.text}

file = json.dumps(Description)
print(file)