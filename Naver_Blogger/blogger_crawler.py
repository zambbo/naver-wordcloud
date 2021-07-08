import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#base url은 해당 포맷을 따라야한다.
#nick_name = 'duswk75'
#nick_name = 'yaesul1205'
nick_name = str(input('블로그 이름을 입력: '))
base_url = f'https://blog.naver.com/PostList.naver?blogId={nick_name}&categoryNo=0&from=postList'

def getNickName(_url):
    nickname = re.findall('blogId=.+',_url)[0][7:]
    am_index = nickname.find("&")
    nickname = nickname[:am_index]
    return nickname

driver = webdriver.Chrome()
driver.get(base_url)
driver.implicitly_wait(1)
wait = WebDriverWait(driver,timeout=5)
bottom_list = []


while True:
    try:
        wait.until(EC.presence_of_element_located,(By.ID,'postBottomTitleListBody'))
        element = driver.find_element_by_id('postBottomTitleListBody')
    except:
        print("bottom error")
        continue
    try:
        wait.until(EC.presence_of_element_located,(By.CSS_SELECTOR,'.next.pcol2._next_category'))
        wait.until(EC.presence_of_all_elements_located,(By.CLASS_NAME,'wrap_td'))
        for elem in element.find_elements_by_tag_name('a'):
            bottom_list.append((elem.get_attribute('href'),elem.text))
        next_button = driver.find_element_by_css_selector('.next.pcol2._next_category')
        print(next_button)
        if next_button:
            next_button.click()
        else:
            break
    except:
        print("bottom click error")
        continue

print(len(bottom_list))
print(bottom_list)
