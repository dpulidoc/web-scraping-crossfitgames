# -*- coding: utf-8 -*-
"""
@author: DPulido
"""
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://games.crossfit.com/leaderboard/open/2021?view=0&division=1&region=0&scaled=0&sort=0')
time.sleep(2)

totalpages=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[3]/div/div[2]/a[6]')
totalpages=int(totalpages.text)
#print (totalpages)
totalpages=20 # he limitado a 20 paginas el scraping ya que en total son 2750

dfT= pd.DataFrame(columns=['rank','fullname','points','country'])

for page in range(totalpages):
    if ((page+1)!=1):
        driver.get('https://games.crossfit.com/leaderboard/open/2021?view=0&division=1&region=0&scaled=0&sort=0&page='+(str(page+1)))
        time.sleep(2)
  
    totalathletes=50 #he seleccionado el total de atletas por página
    for athlete in range(totalathletes):
        #print('athlete: ')
        #print(str(athlete+1))      
        rank= driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/table/tbody/tr['+str(athlete+1)+']/td[1]/div')
        firstnames= driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/table/tbody/tr['+str(athlete+1)+']/td[2]/div/div[1]/div[2]/div[1]')
        lastnames= driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/table/tbody/tr['+str(athlete+1)+']/td[2]/div/div[1]/div[2]/div[2]')
        points = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/table/tbody/tr['+str(athlete+1)+']/td[3]/div')
        country = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[1]/div/table/tbody/tr['+str(athlete+1)+']/td[2]/div/div[1]/div[3]/img')
        region= driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/table/tbody/tr['+str(athlete+1)+']/td[2]/div/div[2]/ul/li[2]')
        region=region.get_attribute("innerHTML")    
        fullname=firstnames.text+' '+lastnames.text
                                           
        #age= driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/table/tbody/tr['+str(athlete+1)+']/td[2]/div/div[2]/ul/li[4]')
        #age=age.get_attribute("innerHTML")
        #age = age.split(" ")
        #age=age[1]
        
        getAttribute = lambda x: x.get_attribute("title")
        countrylist = list(map(getAttribute, country)); countrylist
    
        df=pd.DataFrame({'rank':rank.text,'fullname':fullname,'points':points.text,'country':countrylist,'region':region})
        dfT=pd.concat([dfT, df], ignore_index=True)

#print (dfT)
export_csv = dfT.to_csv (r'C:\Users\David\Desktop\export_crossfit_leaderboard.csv', index = None, header=True)