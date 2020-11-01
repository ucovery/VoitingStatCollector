from selenium import webdriver
from bs4 import BeautifulSoup
import time
import numpy as np

chrome_driver_path = 'E:\\chromedriver_win32\chromedriver.exe'
base_url = 'http://www.krasnodar.vybory.izbirkom.ru/region/krasnodar?action=ik&vrn='
driver = webdriver.Chrome(chrome_driver_path)


def parseIDs(id):
    driver.get(base_url + id)
    time.sleep(1)
    page_code = driver.page_source
    soup = BeautifulSoup(page_code, 'html5lib')
    tags = soup.find_all(['li'])
    for tag in tags:
        tag_name = tag.text
        if (tag_name.find("Участковая избирательная комиссия №") != -1) and len(tag.get("id")) == 13 and len(
                tag_name) < 45:
            print(tag_name + "=" + str(len(tag.get("id"))) + "=" + tag.get("id"))
            uik_ids[tag_name] = isCprfViewerCheck(tag.get("id"))


# Проверяем был ли представитель КПРФ на участке
def isCprfViewerCheck(uic_id):
    driver.get('http://www.krasnodar.vybory.izbirkom.ru/region/krasnodar?action=ik&vrn=' + uic_id)
    time.sleep(1)
    page_code = driver.page_source
    exist = False
    if page_code.find("КОММУНИСТИЧЕСКАЯ ПАРТИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ") != -1:
        exist = True
    return exist


# Список id тиков
tik_ids = ['4234018213637', '4234021205616', '4234020278176', '4234019275163', '22320002012442']
uik_ids = {}

for id in tik_ids:
    parseIDs(id)

np.save('CPRF_is.npy', uik_ids)
