import numpy as np 
import requests 
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time

#set up profile to automatically download files of type excel 
#from: https://stackoverflow.com/questions/37247336/selenium-use-of-firefox-profile
profile = FirefoxProfile()
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
profile.set_preference("browser.download.dir", "/Users/llccf/OneDrive/Dokumente/Hiwi_Jobs_Master/QuantEcon/Felix/Social Security Spain/src_data")
#set up options to create a headless browser
options = Options() 
options.headless = True

#start selenium webdriver
driver = webdriver.Firefox(firefox_profile = profile, options = options)

#set up url 
#url for data from 2003-2009
url_early = 'http://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST8/2341/2683/2684?changeLanguage=es'
#url for data from 2010-2014
url_late = "http://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/est8/2341/2683/3460?changeLanguage=es"

#get url
driver.get(url_early)

#combine xpath to access element of interest 
#this loop: early 
for i in range(3,10):
    year = str(i)
    year_link = 'article' + '[' + year + ']'
    for j in range(1,13):
        month = str(j)
        xpath_1 = '/html/body/div/main/section[2]/div/div/div/div/div[7]/'
        xpath_2 = '/div/div[2]/div/div/div/table/tbody/'
        month_link = 'tr[' + month + ']'
        xpath_3 = '/td[2]/a'
        complete = xpath_1 + year_link + xpath_2 + month_link + xpath_3
        link = driver.find_element_by_xpath(complete)
        link.click()
        print(year + " " + month)

#this loop: late
driver.get(url_late)
for i in range(2,7):
    year = str(i)
    year_link = 'article' + '[' + year + ']'
    for j in range(1,13):
        month = str(j)
        xpath_1 = '/html/body/div/main/section[2]/div/div/div/div/div[7]/'
        xpath_2 = '/div/div[2]/div/div/div/table/tbody/'
        month_link = 'tr[' + month + ']'
        xpath_3 = '/td[2]/a'
        complete = xpath_1 + year_link + xpath_2 + month_link + xpath_3
        link = driver.find_element_by_xpath(complete)
        link.click()
        print(year + " " + month)
