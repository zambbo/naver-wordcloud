import pandas as pd
from datetime import date
import re
#file_name = 'yaesul1205-2021-07-09.csv'
#file_name_list = ['./csvfile/maize210-2021-07-13.csv','./csvfile/nora_nori-2021-07-13.csv','./csvfile/wseblove-2021-07-13.csv']
# category_list = [('제작',['보석십자수', '미니어처', '펀치 니들', '3d펜', '3d프린터', '가죽공예', '가방 만들기', '양모펠트', '프랑스 자수', '스크래치 북', 'DIY']),
# ('생활',['LED조명', '무드등', '칼림바', '오르골', '발난로', '우산', '캡슐 세제']),
# ('측정',['전자저울', '산소포화도 측정기', '소음 측정기', '거리 측정기', '온습도계', '적외선 온도계', '높이 측정기', '타이머', '유수분 측정기']),
# ('메카',['아두이노', '라즈베리 파이', '마이크로 비트', '컴퓨터 부품', '커넥터'])]

def saveCategoryCSVFromBlogger_csv(_file_name,_category_list):

    nick_name = re.findall('[^-]+-{1}',_file_name)[0][:-1]

    category_name = ['A','B']
    category_dataframe_list = []
    base_df = pd.read_csv(_file_name)



    for category_ in _category_list:
        category_items = category_[1]
        category_name = category_[0]
        category = []
        for item in category_items:
            item_bool = base_df['Title'].apply(lambda x: item in x)
            item_df = base_df[item_bool]
            category.append(item_df)    
        category_dataframe_list.append((category_name,category))

    for category,category_dataframe_ in zip(_category_list,category_dataframe_list):
        category_dataframe_name = category_dataframe_[0]
        category_dataframe_items = category_dataframe_[1]

        category_input = dict()
        item_len = len(category[1])
        category_item_mulcol = list(category_dataframe_items[0].columns)[1:]*item_len
        category_item_mulcol = [value + category[1][int(idx/2)] for idx,value in enumerate(category_item_mulcol)]

        idx = 0
        for category_df_ in category_dataframe_items:
            title = category_df_['Title'].tolist()
            link = category_df_['Link'].tolist()
            category_input[category_item_mulcol[idx]] = link
            category_input[category_item_mulcol[idx+1]]= title
            idx = idx + 2

        category_df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in category_input.items()]))
        category_df.to_csv(f'{nick_name}-{category_dataframe_name}-{date.today().isoformat()}.csv')

# _blogger_posts : ex) [('A',[('Link1','Title1'),('Link2','Title2')]),('B',[('Link1','Title1'),('Link2','Title2')])]
# category_lists : ex) [('A',['A1','A2','A3']),('B',['B1','B2','B3'])]
test_blogger_post = [('chulsu',[('a','고양이'),('b','고먐미')]),('younghee',[('c','아이폰'),('d','마이폰')])]

def getCategoryFromBlogger_tuple(_blogger_posts,category_lists):
    nick_item_dict = dict()
    for bloggers in _blogger_posts:
        nick_name = bloggers[0]
        link_title_list = bloggers[1]

        title_lists = [post_link[1] for post_link in link_title_list]
        for category in category_lists:
            for item in category[1]:
                title_item_exists_list = [title for title in title_lists if item in title]
                item_len = len(title_item_exists_list)
                if nick_item_dict.get(nick_name) is None:
                    nick_item_dict[nick_name] = []
                    nick_item_dict[nick_name].append((item,item_len))
                    continue
                nick_item_dict[nick_name].append((item,item_len))
    
    return nick_item_dict

if __name__ == '__main__':
    for filename in file_name_list:
        saveCategoryCSVFromBlogger_csv(filename,category_list)