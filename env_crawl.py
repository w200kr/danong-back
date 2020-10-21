#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup as bs
from IPython import embed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import requests
import re
import datetime
import time
import json
import pandas as pd

base_url = 'http://www.nongsaro.go.kr/portal/ps/psa/psab/psabe/openApiSoilVrifyLst.ps?menuId=PS03329'

location_text = '서울특별시 강남구 논현동 69'

location_texts = location_text.split()

# exclude 리
if len(location_texts)==4:
    [sido, sigungu, townmyeondong, jibn] = location_texts
elif len(location_texts)==5:
    [sido, sigungu, townmyeondong, ri, jibn] = location_texts

def webdriver_init(base_url):
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # driver = webdriver.Chrome("./chromedriver", options=options)
    driver = webdriver.Chrome('./chromedriver')
    driver.get(base_url)
    return driver

driver = webdriver_init(base_url)

sido_select = Select(driver.find_element_by_id('siDoLst'))
sido_select.select_by_visible_text(sido)

sigungu_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="siGunGuLst"]/option[2]')))
sigungu_select = Select(sigungu_option.find_element_by_xpath('..'))
sigungu_select.select_by_visible_text(sigungu)

townmyeondong_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="townMyeonDongLst"]/option[2]')))
townmyeondong_select = Select(townmyeondong_option.find_element_by_xpath('..'))
townmyeondong_select.select_by_visible_text(townmyeondong)

try:
    ri
    ri_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="riLst"]/option[2]')))
    ri_select = Select(townmyeondong_option.find_element_by_xpath('..'))
    ri_select.select_by_visible_text(townmyeondong)
except NameError:
    pass

jibn_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sel_jibn"]/option[2]')))
jibn_select = Select(jibn_option.find_element_by_xpath('..'))
soup = bs(driver.page_source, 'html.parser')
select_soup = soup.find('select',{'id':'sel_jibn'})
jibn_select.select_by_visible_text(select_soup.find(text=re.compile(jibn)))

result_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="jibun_div"]')))
soup = bs(driver.page_source, 'html.parser')
result_div_html = soup.find('div', {'id': 'jibun_div'})

print result_div_html

# embed()

driver.quit()

# TODO : 세종시 예외
# TODO : 주소 일치하지 않을 경우 혹은 명칭이 다를 경우(서울특별시 or 서울시)