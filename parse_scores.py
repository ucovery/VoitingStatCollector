from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import time

#Парсер статистики выборов в краснодарском крае
chrome_driver_path = 'E:\\chromedriver_win32\chromedriver.exe'
base_url='http://www.krasnodar.vybory.izbirkom.ru/region/region/krasnodar?action=show&root=1&tvd=4234220141772&vrn=4234220141768&region=23&global=&sub_region=23&prver=2&pronetvd=1&vibid=4234220141772&type=381'

driver = webdriver.Chrome(chrome_driver_path)
driver.get(base_url)

# При первом открытии сайта вводим капчу в браузере
input('Капча введена?')
page_code = driver.page_source
soup = BeautifulSoup(page_code, 'html5lib')
scores_array = {}

# Парсим структуру
def parseStructure(tblnum):
    flag_iterator = 0
    uic_values = []
    result_values = []
    mytbl = table[tblnum]
    rows = mytbl.findChildren(['th', 'tr'])
    for row in rows:
        flag_iterator += 1
        if flag_iterator == 21:
            cells = row.findChildren('td')
            for cell in cells:
                value = cell.text
                uic_values.append(value)
        if flag_iterator == 39:
            cells = row.findChildren('td')
            for cell in cells:
                value = cell.text
                result_values.append(value.strip())
    for i, value in enumerate(uic_values):
        scores_array[value] = result_values[i]


hrefs_count = 0
hrefs = []

for link in soup.find_all('a'):
    hrefs_count += 1
    if hrefs_count > 10:
        hrefs.append(link.get('href'))
print("Ссылки собраны!")

for i in hrefs:
    driver.get(i)
    time.sleep(1)
    print('Загрузка данных...')
    page_code = driver.page_source
    soup = BeautifulSoup(page_code, 'html5lib')
    table = soup.findChildren('table')
    mytbl = table[7]
    rows = mytbl.findChildren(['th', 'tr'])
    parseStructure(7)

np.save('VibKRD.npy', scores_array)
