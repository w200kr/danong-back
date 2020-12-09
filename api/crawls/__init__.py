from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

from IPython import embed

import requests
import random
import os

mac_driver_path = os.path.dirname(os.path.abspath(__file__))+"/chromedriver_mac"
linux_driver_path = os.path.dirname(os.path.abspath(__file__))+"/chromedriver_linux"

base_url = 'http://www.nongsaro.go.kr/portal/ps/psa/psab/psabe/openApiSoilVrifyLst.ps?menuId=PS03329'


class Crawler(object):
    """docstring for Crawler"""
    def __init__(self):
        super(Crawler, self).__init__()

        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')

        try:
            self.driver = webdriver.Chrome(mac_driver_path, options=options)
        except Exception as e:
            self.driver = webdriver.Chrome(linux_driver_path, options=options)
            # raise e
        self.driver.get(base_url)

        self.sido_select = Select(self.driver.find_element_by_id('siDoLst'))
        self.sigungu_select = Select(self.driver.find_element_by_id('siGunGuLst'))
        self.townMyeonDong_select = Select(self.driver.find_element_by_id('townMyeonDongLst'))
        self.ri_select = Select(self.driver.find_element_by_id('riLst'))
        self.jibn_select = Select(self.driver.find_element_by_id('sel_jibn'))

        self.geocode_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="
        self.headers = {
            'X-NCP-APIGW-API-KEY-ID': 'm11ogby6ag',
            'X-NCP-APIGW-API-KEY': 'G8nc8zH5sP4pg8ZVMYETnLoReXCfx04vgNKvwsPE',
        }

    def select_by_text(self, select, text):
        if text is None or len(text)==0:
            return 
        text = text.replace(' ', '')

        for index, option in enumerate(select.options):
            if text in option.text:
                select.select_by_index(index)
                # self.wait_for_load()
                return 

    def select_by_random(self, select):
        if len(select.options) > 1:
            random_int = random.randint(1, len(select.options)-1)
            select.select_by_index(random_int)
            self.wait_for_load()

    def wait_for_load(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(EC.staleness_of(driver.find_element_by_css_selector('div.blockPage')))
        
    def remove_empty_objs(self, unfiltered_list):
        return list(filter(lambda info: len(info['longName'])!=0, unfiltered_list))

    def find_obj(self, target_list, key, value):
        return next( (obj for obj in target_list if obj[key][0]==value), None)

    def get_value(self, obj, key):
        if obj is not None:
            return obj[key]

    # def get_key_by_value(self, obj, value):
    #     return [ obj]

    # def remove_blank(self, string):
    #     return string.replace(' ', '')

    def lookup_geocode(self, address):
        url = self.geocode_url+address
        response = requests.get(url, headers=self.headers)
        response_json = response.json()

        # return {
        #     'lng': response['addresses'][0]['x'],
        #     'lat': response['addresses'][0]['y']
        # }
        if response.status_code == 200 and response_json['status'] == 'OK':
            if response_json['meta']['totalCount']>0:
                return response_json['addresses'][0]
            else:
                raise Exception('검색 결과가 없습니다.')
        else:
            raise Exception('정상적인 응답을 받지 못했습니다.')


    # step 1. 입력된 주소값을 Naver Geocode API로 조회
    # step 2. 정상적으로 조회된 결과가 존재하면 해당 지번 주소를 농사로 페이지에 입력 후 결과를 크롤링
    def lookup_nongsaro(self, address):
        driver = self.driver
        try:
            searched_address = self.lookup_geocode(address)
            geo_position = {
                'lng': searched_address['x'],
                'lat': searched_address['y']
            }
            address_elements = searched_address['addressElements']
        except Exception as e:
            raise e

        filtered_list = self.remove_empty_objs(address_elements)

        sido_text = self.get_value( self.find_obj(filtered_list, 'types', 'SIDO'), 'longName' )
        sigungu_text = self.get_value( self.find_obj(filtered_list, 'types', 'SIGUGUN'), 'longName' )
        townMyeonDong_text = self.get_value( self.find_obj(filtered_list, 'types', 'DONGMYUN'), 'longName' )
        ri_text = self.get_value( self.find_obj(filtered_list, 'types', 'RI'), 'longName' )
        jibn_text = self.get_value( self.find_obj(filtered_list, 'types', 'LAND_NUMBER'), 'longName' )

        # self.select_by_text(self.sido_select, sido_text)
        # self.select_by_text(self.sigungu_select, sigungu_text)
        # self.select_by_text(self.townMyeonDong_select, townMyeonDong_text)
        # self.select_by_text(self.ri_select, ri_text)
        # self.select_by_text(self.jibn_select, jibn_text)

        self.select_by_text(self.sido_select, sido_text)
        if sido_text=='세종특별자치시':
            raise Exception('농사로 토양검정정보에서 세종특별자치시가 저장되지 않았습니다.')
        else:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#siGunGuLst > option:nth-child(2)")))

            self.select_by_text(self.sigungu_select, sigungu_text)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#townMyeonDongLst > option:nth-child(2)")))

        self.select_by_text(self.townMyeonDong_select, townMyeonDong_text)
        if townMyeonDong_text[-1]=='동':
            pass
        else:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#riLst > option:nth-child(2)")))

            self.select_by_text(self.ri_select, ri_text)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#jibn_tr")))

        self.select_by_text(self.jibn_select, jibn_text)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jibun_div")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jibun_div"]/div[4]')))


        # address = driver.find_element_by_xpath('//*[@id="jibun_div"]/div[2]/table/tbody/tr/td').text
        aptitude_div = driver.find_element_by_xpath('//*[@id="jibun_div"]/div[4]')
        soup = bs(aptitude_div.get_attribute('innerHTML'), features="html.parser")
    
        response = {
            'address': searched_address['jibunAddress'],
            'aptitude_table': str(soup).replace('\n', ''),
            **geo_position,
        }

        return response