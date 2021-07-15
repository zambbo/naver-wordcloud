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
class NaverBloggerCrawler:

    def saveAllPostsOfBlogger(self, _nickname):
        posts = self.crawling_blogger(_nickname)
        blogger_df = pd.DataFrame(posts,columns=['Link','Title'])
        blogger_df.to_csv(f'{_nickname}-{date.today().isoformat()}.csv')

    def getAllPostsOfBloggers(self, _nickname_list):

        blogger_posts_list = []
        for nickname in _nickname_list:
            posts = self.crawling_blogger(nickname)
            blogger_posts_list.append((nickname,posts))
            time.sleep(2)
        return blogger_posts_list

    def crawling_blogger(self, _nickname):
        base_url = f'https://blog.naver.com/PostList.naver?blogId={_nickname}&categoryNo=0&from=postList'
        print('start!')
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("--dns-prefetch-disable")
        driver = webdriver.Chrome('chromedriver',options=options)
        driver.get(base_url)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver,timeout=10,poll_frequency=0.1)
        bottom_list = []

        idx = 0
        while True:
            #100개 제한
            if idx>100:
                break
            try:
                print(f'\r{idx}',end='')
                idx = idx + 1
                try:
                    wait.until(EC.presence_of_element_located,(By.XPATH,'//*[@id="postBottomTitleListBody"]'))
                    wait.until(EC.presence_of_element_located,(By.CSS_SELECTOR,'.date.pcol2'))
                    _date = driver.find_element_by_css_selector('.date.pcol2')
                    element = driver.find_element_by_xpath('//*[@id="postBottomTitleListBody"]')
                except StaleElementReferenceException:
                    element = driver.find_element_by_xpath('//*[@id="postBottomTitleListBody"]')
                    _date = driver.find_element_by_css_selector('.date.pcol2')
                except TimeoutException:
                    print("TimeoutException")
                    break
                except:
                    print("unknown error")
                    break
                finally:
                    try:
                        _date = int(_date.text.split('.')[0])
                        #print("\n",date,sep='')
                    except:
                        _date = 2021
                    if _date<2020:
                        print('\n not recent posting!')
                        break
                    for elem in element.find_elements_by_tag_name('a'):
                        bottom_list.append((elem.get_attribute('href'),elem.text))
                try:
                    wait.until(EC.element_to_be_clickable,(By.CSS_SELECTOR,'.next.pcol2._next_category'))
                    next_button = driver.find_element_by_css_selector('.next.pcol2._next_category')
                except StaleElementReferenceException:
                    next_button = driver.find_element_by_css_selector('.next.pcol2._next_category')
                except:
                    print("unknown error")
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
                blogger_df = pd.DataFrame(bottom_list,columns=['Link','Title'])
                blogger_df.to_csv(f'./temp_csv/{_nickname}-{date.today().isoformat()}.csv')
                return bottom_list

        print(bottom_list)
        print('finish!')
        driver.quit()
        blogger_df = pd.DataFrame(bottom_list,columns=['Link','Title'])
        blogger_df.to_csv(f'./temp_csv/{_nickname}-{date.today().isoformat()}.csv')
        return bottom_list

if __name__ == '__main__':
    for idx,nick_name in enumerate(nick_name_list):
        bloggerCrawler = NaverBloggerCrawler()
        bloggerCrawler.saveAllPostsOfBlogger(nick_name)
        print(f'{idx+1}blogger finish!')
        time.sleep(2)