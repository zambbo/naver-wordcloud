from blogger_crawler import getAllPostsOfBloggers
from make_category import getCategoryFromBlogger_tuple
import pandas as pd
import numpy as np
from datetime import date

test_category_list = [('뷰티',['네일','샴푸','선크림','틴트','에센스']),
('반려동물',['고양이','강아지','집사']),
('IT',['키보드','마우스','아이폰','카메라'])] 

nick_name_list = ['haniyamyam','beauvelye','wlgysnl23','oksubenne','wj_2169','eve14eve','bichon-haru','gamja321','nce0623','kimcoco1']

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

def run():
    blogger_posts = getAllPostsOfBloggers(nick_name_list)
    blogger_item_dict = getCategoryFromBlogger_tuple(blogger_posts,test_category_list)
    saveCSV(blogger_item_dict,test_category_list)

if __name__ == '__main__':
    run()