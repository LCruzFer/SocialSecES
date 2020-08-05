import numpy as np 
from datetime import datetime
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time


"""
Use a very basic web scraping code to automatically download the files containing data on municipios from 
http://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST8/2341/2683?changeLanguage=es
Note that there are two links provided on this website, which are referred to below 
as url_early and url_late 
"""

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
url_early = "http://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST8/2341/2683/2684?changeLanguage=es"
#url for data from 2010-2014
url_late = "http://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/est8/2341/2683/3460?changeLanguage=es"

#get url
driver.get(url_early)

#combine xpath to access element of interest 
"""
Explainer: 

Open url_early in your browser (for url_late the process is the same) and open the inspector via the Web Developer tools
(Firefox: Settings -> Web Developer -> Inspector; for other please Google) and right click on the download link of the very first file. 
Then right click on the highlighted (Firefox: blue) part in the Inspector window at the bottom. Select "Copy Xpath". 

This returns as of 05.08.20: 
/html/body/div[1]/main/section[2]/div/div/div/div/div[7]/article[3]/div/div[2]/div/div/div/table/tbody/tr[1]/td[2]/a
This is the xpath to the download link for the dataset of December, 2009

Then repeat this procedure for the last link on this page. 

This returns as of 05.08.20: 
/html/body/div[1]/main/section[2]/div/div/div/div/div[7]/article[9]/div/div[2]/div/div/div/table/tbody/tr[12]/td[2]/a
This is the xpath to the download link for the dataset of January, 2003 

As you can see, there are 2 differences: article[3] for year 2009 and article[9] for year 2003 
as well as tr[1] for December and tr[12] for January (at the end of the path). Hence, below loops 
over 3 to 9 and 1 to 12 and inserts the respective combination in the rest of the xpath element. This element 
is then searched for in the selenium session and clicked on which automatically starts the download. 

If more data becomes available (at date of writing url_late shows data up to 2014) this procedure must be repeated and 
the outer loop over the year number (referred to in the article elemen) must be adjusted accordingly. 
"""

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
