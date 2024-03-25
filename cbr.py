from bs4 import BeautifulSoup
import requests
from datetime import date


today = date.today()
d1 = today.strftime("%d/%m/%Y")
url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req='
#d1 = input("Введите желаемую дату? (дд/мм/гггг): ")

urldate = url+d1

page = requests.get(urldate)
print('Status code: ', page.status_code)
print(urldate, f'\nСписок курсов валют ЦБ РФ по состоянию на {d1}:')

filtered = []
allNews = []

soup = BeautifulSoup(page.text.encode("windows-1251"), features="xml")
#print(soup.prettify())      #эта команда выводит всю страницу как xml в красивом виде

allCurrency = soup.findAll('Valute')

val_kod = []
val_shifre = []
val_quantity = []
val_name = []
val_cost = []

for data in allCurrency:
    if data.findAll('Valute/Valute') is not None:        
        filtered.append(data.text)
        s = 0
        for child in data.contents:
            s += 1
            if s == 1: val_kod.append(child.string)
            if s == 2: val_shifre.append(child.string)
            if s == 3: val_quantity.append(child.string)
            if s == 4: val_name.append(child.string)
            if s == 5: val_cost.append(child.string)


count = len(val_kod)

f = open('currency.txt', 'w+')

for i in range(count):
    index = f'{val_kod[i]:4}{val_shifre[i] :4}{val_quantity[i] :6}{val_name[i] :42}{{0:>8}}'.format(val_cost[i])
    f.write(index + '\n')
    print (f'{val_kod[i]:4}{val_shifre[i] :4}{val_quantity[i] :6}{val_name[i] :42}{{0:>8}}'.format(val_cost[i]))
f.close()
