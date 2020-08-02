import numpy as np 
import requests 
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options

url = 'http://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST8/2341/2683/2684'
options = Options() 
#below is from: http://www.allselenium.info/file-downloads-python-selenium-webdriver/
options.set_preference("browser.download.folderList",2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir","/data")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")
options.headless = True
driver = webdriver.Firefox(options = options)
driver.get(url)

for i in range(3,10):
    i = 3
    year = str(i)
    year_link = 'article' + '[' + year + ']'
    for j in range(1,13):
        j = 1
        month = str(j)
        xpath_1 = '/html/body/div/main/section[2]/div/div/div/div/div[7]/'
        xpath_2 = '/div/div[2]/div/div/div/table/tbody/'
        month_link = 'tr[' + month + ']'
        xpath_3 = '/td[2]/a'
        complete = xpath_1 + year_link + xpath_2 + month_link + xpath_3
        link = driver.find_element_by_xpath(complete)
        link.click()

/html/body/div/main/section[2]/div/div/div/div/div[7]/article[4]/div/div[2]/div/div/div/table/tbody/tr[3]/td[2]/a
complete