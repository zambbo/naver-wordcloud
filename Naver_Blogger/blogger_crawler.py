import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options

import time
#base url은 해당 포맷을 따라야한다.
#nick_name = 'duswk75'
#nick_name = 'yaesul1205'
nick_name = str(input('블로그 이름을 입력: '))
base_url = f'https://blog.naver.com/PostList.naver?blogId={nick_name}&categoryNo=0&from=postList'

# def getNickName(_url):
#     nickname = re.findall('blogId=.+',_url)[0][7:]
#     am_index = nickname.find("&")
#     nickname = nickname[:am_index]
#     return nickname
options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
driver.get(base_url)
driver.implicitly_wait(10)
wait = WebDriverWait(driver,timeout=5,poll_frequency=0.1)
bottom_list = []

# pre_bottomPost = driver.find_element_by_id('postBottomTitleListBody')
# pre_button = driver.find_element_by_css_selector('.next.pcol2._next_category')

idx = 0
while True:
    print(f'\r{idx}',end='')
    idx = idx + 1
    try:
        wait.until(EC.presence_of_element_located,(By.ID,'postBottomTitleListBody'))
        element = driver.find_element_by_id('postBottomTitleListBody')
    except StaleElementReferenceException:
        element = driver.find_element_by_id('postBottomTitleListBody')
    except:
        print("bottom error")
        break
    finally:
        for elem in element.find_elements_by_tag_name('a'):
            bottom_list.append((elem.get_attribute('href'),elem.text))

    try:
        wait.until(EC.element_to_be_clickable,(By.CSS_SELECTOR,'.next.pcol2._next_category'))
        next_button = driver.find_element_by_css_selector('.next.pcol2._next_category')
    except StaleElementReferenceException:
        next_button = driver.find_element_by_css_selector('.next.pcol2._next_category')
    except:
        print("bottom click error")
        break
    finally:
        next_button.click()
        try:
            wait.until(lambda x : x.find_element_by_css_selector('.next.pcol2._next_category') != next_button)
        except TimeoutException as e:
            print(e)
            break
print(len(bottom_list))
print(bottom_list)
