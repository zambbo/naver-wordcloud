from blogger_crawler import NaverBloggerCrawler
from make_category import Category
import pandas as pd
import numpy as np
from datetime import date
import re
from utils import *
# test_category_list = [('뷰티',['보석십자수','전자저울','캡슐세제','틴트','에센스']),
# ('반려동물',['고양이','강아지','집사']),
# ('IT',['키보드','마우스','아이폰','카메라'])] 
category_list = [('제작',['보석십자수', '미니어처', '펀치 니들', '3d펜', '3d프린터', '가죽공예', '가방 만들기', '양모펠트', '프랑스 자수', '스크래치 북', 'DIY']),
('생활',['LED조명', '무드등', '칼림바', '오르골', '발난로', '우산', '캡슐 세제']),
('측정',['전자저울', '산소포화도 측정기', '소음 측정기', '거리 측정기', '온습도계', '적외선 온도계', '높이 측정기', '타이머', '유수분 측정기']),
('메카',['아두이노', '라즈베리 파이', '마이크로 비트', '컴퓨터 부품', '커넥터'])]
#nick_name_list = ['haniyamyam','beauvelye','wlgysnl23','oksubenne','wj_2169','eve14eve','bichon-haru','gamja321','nce0623','kimcoco1']
file_name_list = ['./csvfile/보석십자수2021-07-06.csv','./csvfile/전자저울2021-07-07.csv','./csvfile/캡슐세제2021-07-01.csv']

path = './temp_csv'

def get_nick_name_list(_df):
    urls = _df['Post URL']
    urls = [re.findall('com\/.*\?',x)[0][4:-1] for x in urls]
    return urls

def get_nick_name_list_from_filename_list(_filenamelist):
    nick_name_list = []
    for filename in _filenamelist:
        df = pd.read_csv(filename)

        df = df.iloc[:,:100]
        nick_names = get_nick_name_list(df)
        nick_name_list.extend(nick_names)
    return nick_name_list

def makeItemListFromCategoryList(_category_lists):
    item_list = []
    for category_item in _category_lists:
        items = category_item[1]
        item_list.extend(items)
    return item_list

def saveCSV(_blogger_item_dict,_category_list):

    items = makeItemListFromCategoryList(_category_list)
    item_columns = np.array(items)
    bloggers = []
    item_posting_score_2d = []

    for nickname,item_posting_list in _blogger_item_dict.items():
        bloggers.append(nickname)
        item_posting_list = [item_posting[1] for item_posting in item_posting_list]
        item_posting_score_2d.append(item_posting_list)    
    item_posting_score_2d = np.array(item_posting_score_2d)
    df = pd.DataFrame(item_posting_score_2d,columns=item_columns,index=bloggers)
    df.to_csv(f'recommender-{date.today().isoformat()}.csv')
    print('finish!')

def df2bloggerPosts(_df):
    link_list = _df['Link'].tolist()
    title_list = _df['Title'].tolist()

    link_title_list = [(link,title) for link,title in zip(link_list,title_list)]
    return link_title_list

def crawlAllBlogAndSave():
    nick_name_list = get_nick_name_list_from_filename_list(file_name_list)
    blogger_crawler = NaverBloggerCrawler()
    blogger_posts = blogger_crawler.getAllPostsOfBloggers(nick_name_list)
    print('finish get bloggers posts')
    category = Category(category_list)
    blogger_item_dict = category.getCategoryFromBlogger_tuple(blogger_posts)
    saveCSV(blogger_item_dict,category_list)
    print('finish saving!')

def saveCategoryFromFiles(_path):
    file_list = getFileListFromPath(_path)
    nickname_list = [getNickNameFromFileName(file) for file in file_list]
    blogger_posts = []
    for nickname,filename in zip(nickname_list,file_list):
        df = pd.read_csv('./temp_csv/'+filename)
        posts = df2bloggerPosts(df)
        blogger_posts.append((nickname,posts))
    category = Category(category_list)
    blogger_item_dict = category.getCategoryFromBlogger_tuple(blogger_posts)
    saveCSV(blogger_item_dict,category_list)

def run():
    saveCategoryFromFiles(path)

if __name__ == '__main__':
    run()