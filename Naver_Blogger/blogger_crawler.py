from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import date

import time
#base url은 해당 포맷을 따라야한다.
#nick_name = 'duswk75'
#nick_name = 'yaesul1205'

#nick_name = str(input('블로그 이름을 입력: '))

nick_name_list = ['nora_nori','serom11','maize210','wseblove','dream8503']
#nick_name_list = ['haniyamyam','beauvelye','wlgysnl23','oksubenne','wj_2169','eve14eve','bichon-haru','gamja321','nce0623','kimcoco1']
# def getNickName(_url):
#     nickname = re.findall('blogId=.+',_url)[0][7:]
#     am_index = nickname.find("&")
#     nickname = nickname[:am_index]
#     return nickname
def saveAllPostsOfBlogger(_nickname):
    posts = crawling_blogger(_nickname)
    blogger_df = pd.DataFrame(posts,columns=['Link','Title'])
    blogger_df.to_csv(f'{_nickname}-{date.today().isoformat()}.csv')

def getAllPostsOfBloggers(_nickname_list):

    blogger_posts_list = []
    for nickname in _nickname_list:
        posts = crawling_blogger(nickname)
        blogger_posts_list.append((nickname,posts))
        time.sleep(2)
    return blogger_posts_list

def crawling_blogger(_nickname):
    base_url = f'https://blog.naver.com/PostList.naver?blogId={_nickname}&categoryNo=0&from=postList'
    print('start!')
    options = Options()
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options)
    driver.get(base_url)
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver,timeout=10,poll_frequency=0.1)
    bottom_list = []

    idx = 0
    while True:
        try:
            print(f'\r{idx}',end='')
            idx = idx + 1
            try:
                wait.until(EC.presence_of_element_located,(By.ID,'bottom-list'))
                date = driver.find_element_by_css_selector('.date.pcol2')
                element = driver.find_element_by_id('bottom-list')
            except StaleElementReferenceException:
                element = driver.find_element_by_id('bottom-list')
                date = driver.find_element_by_css_selector('.date.pcol2')
            except:
                print("bottom error")
                break
            finally:
                try:
                    date = int(date.text.split('.')[0])
                except:
                    date = 2021
                if date<2016:
                    break
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
        except:
            print('Cannot crawl this blogger.')
            driver.quit()
            return []

    print(len(bottom_list))
    print(bottom_list)
    print('finish!')
    driver.quit()
    return bottom_list

if __name__ == '__main__':
    for idx,nick_name in enumerate(nick_name_list):
        saveAllPostsOfBlogger(nick_name)
        print(f'{idx+1}blogger finish!')
        time.sleep(2)