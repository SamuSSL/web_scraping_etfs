from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from pprint import pprint
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.etf.com/etfanalytics/etf-screener'

driver.get(url)

response = requests.get(url)

time.sleep(5)

botao_100 =  driver.find_element('xpath', '''/html/body/div[2]/div/div[1]/main/div/section/div[2]/div[2]/div[3]/div
 /article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[5]/button''')

driver.execute_script('arguments[0].click();', botao_100)

num_pags = driver.find_element('xpath', '''/html/body/div[2]/div/div[1]/main/div/section/div[2]/div[2]/div[3]/div/article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/ul/li[8]/a''')

num_pags = int(num_pags.text)

biblioteca_tabelas = []

for pag in range(0, num_pags):

    tabela = driver.find_element('xpath', '''/html/body/div[2]/div/div[1]/main/div/section/div[2]/div[2]
    /div[3]/div/article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/div[1]/div/div[1]/table''')

    tabela_html = tabela.get_attribute('outerHTML')

    tabela_organizada = pd.read_html(tabela_html)[0]

    biblioteca_tabelas.append(tabela_organizada)
    
    try:
        botao_avancar = driver.find_element(By.LINK_TEXT, 'Next')
    except:
        pass
    
    driver.execute_script('arguments[0].click();', botao_avancar)
    
    bd_completa_basico = pd.concat(biblioteca_tabelas)


botao_performance = driver.find_element('xpath', '''/html/body/div[2]/div/div[1]/main/div/section/div[2]
/div[2]/div[3]/div/article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/ul/li[2]''')

driver.execute_script('arguments[0].click();', botao_performance)

biblioteca_tabelas = []

for pag in range(0, num_pags):

    tabela = driver.find_element('xpath', '''/html/body/div[2]/div/div[1]/main/div/section/div[2]/div[2]
    /div[3]/div/article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[1]/table''')

    tabela_html = tabela.get_attribute('outerHTML')

    tabela_organizada = pd.read_html(tabela_html)[0]

    biblioteca_tabelas.append(tabela_organizada)
    
    try:
        botao_avancar = driver.find_element(By.LINK_TEXT, 'Next')
    except:
        pass
    
    driver.execute_script('arguments[0].click();', botao_avancar)
    
    bd_completa_performance = pd.concat(biblioteca_tabelas)


driver.quit()

bd_completa_basico = bd_completa_basico.set_index('Ticker')
bd_completa_basico

bd_completa_performance = bd_completa_performance.set_index('Ticker')
bd_completa_performance

bd_completa_performance = bd_completa_performance[['1 YR', '5 YR', '10 YR']]
bd_completa_performance

bd_final = bd_completa_basico.join(bd_completa_performance)

bd_final.to_excel('Dados ETFs.xlsx')