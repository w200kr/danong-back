#-*- coding: utf-8 -*-
from __future__ import unicode_literals

# from bs4 import BeautifulSoup as bs
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
# import pandas as pd



# 크롬 브라우저 이용해서 크롤링을 수행한다.
def webdriver_init(base_url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome("./chromedriver", options=options)
    # driver = webdriver.Chrome('./chromedriver')
    driver.get(base_url)
    return driver


# def get_random_addresses(addresses_num):
#     base_url = 'http://www.nongsaro.go.kr/portal/ps/psa/psab/psabe/openApiSoilVrifyLst.ps?menuId=PS03329'

#     driver = webdriver_init(base_url)

    

    # 시/도 선택항을 브라우저 상에서 가져온다.
    sido_select = Select(driver.find_element_by_id('siDoLst'))
    # location_text의 '서울특별시'를 선택한다. 
    sido_select.select_by_visible_text(sido)

    # sido_select 값이 설정되면 시/군/구 선택항의 값이 세팅될때까지 시간이 걸린다.
    # 해당 시간을 최대 10초 기다린다. 그전에 시/군/구 선택항의 선택지가 로딩되면 다음 동작을 실행한다.
    sigungu_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="siGunGuLst"]/option[2]')))
    # 시/군/구 선택항을 브라우저 상에서 가져온다.
    sigungu_select = Select(sigungu_option.find_element_by_xpath('..'))
    # location_text의 '강남구'를 선택한다. 
    sigungu_select.select_by_visible_text(sigungu)

    # 이하 반복


    # 해당 시간을 최대 10초 기다린다. 그전에 읍/면/동 선택항의 선택지가 로딩되면 다음 동작을 실행한다.
    townmyeondong_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="townMyeonDongLst"]/option[2]')))
    # 읍/면/동 선택항을 브라우저 상에서 가져온다.
    townmyeondong_select = Select(townmyeondong_option.find_element_by_xpath('..'))
    # location_text의 '논현동'을 선택한다. 
    townmyeondong_select.select_by_visible_text(townmyeondong)




# # 크롤링할 농사로 서비스 url
# base_url = 'http://www.nongsaro.go.kr/portal/ps/psa/psab/psabe/openApiSoilVrifyLst.ps?menuId=PS03329'
# # 농지 주소
# location_text = '서울특별시 강남구 논현동 69'
# # 공백으로 농지 주소를 나눈다. ['서울특별시', '강남구', '논현동', '69]'
# location_texts = location_text.split()

# # '리' 제외 
# if len(location_texts)==4:
#     [sido, sigungu, townmyeondong, jibn] = location_texts
# # '리' 포함 ex) 경기도 남양주시 퇴계원면 ~~리 12-34
# elif len(location_texts)==5:
#     [sido, sigungu, townmyeondong, ri, jibn] = location_texts


# driver = webdriver_init(base_url)


# # 시/도 선택항을 브라우저 상에서 가져온다.
# sido_select = Select(driver.find_element_by_id('siDoLst'))
# # location_text의 '서울특별시'를 선택한다. 
# sido_select.select_by_visible_text(sido)

# # sido_select 값이 설정되면 시/군/구 선택항의 값이 세팅될때까지 시간이 걸린다.
# # 해당 시간을 최대 10초 기다린다. 그전에 시/군/구 선택항의 선택지가 로딩되면 다음 동작을 실행한다.
# sigungu_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="siGunGuLst"]/option[2]')))
# # 시/군/구 선택항을 브라우저 상에서 가져온다.
# sigungu_select = Select(sigungu_option.find_element_by_xpath('..'))
# # location_text의 '강남구'를 선택한다. 
# sigungu_select.select_by_visible_text(sigungu)

# # 이하 반복


# # 해당 시간을 최대 10초 기다린다. 그전에 읍/면/동 선택항의 선택지가 로딩되면 다음 동작을 실행한다.
# townmyeondong_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="townMyeonDongLst"]/option[2]')))
# # 읍/면/동 선택항을 브라우저 상에서 가져온다.
# townmyeondong_select = Select(townmyeondong_option.find_element_by_xpath('..'))
# # location_text의 '논현동'을 선택한다. 
# townmyeondong_select.select_by_visible_text(townmyeondong)

# try:
#     ri
#     ri_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="riLst"]/option[2]')))
#     ri_select = Select(townmyeondong_option.find_element_by_xpath('..'))
#     ri_select.select_by_visible_text(townmyeondong)
# except NameError:
#     pass

# jibn_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sel_jibn"]/option[2]')))
# jibn_select = Select(jibn_option.find_element_by_xpath('..'))
# soup = bs(driver.page_source, 'html.parser')
# select_soup = soup.find('select',{'id':'sel_jibn'})
# jibn_select.select_by_visible_text(select_soup.find(text=re.compile(jibn)))

# result_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="jibun_div"]')))
# soup = bs(driver.page_source, 'html.parser')
# result_div_html = soup.find('div', {'id': 'jibun_div'})

# print result_div_html

# # embed()

# driver.quit()

# # TODO : 세종시 예외
# # TODO : 주소 일치하지 않을 경우 혹은 명칭이 다를 경우(서울특별시 or 서울시)

try:
    pass
except Exception as e:
    raise e