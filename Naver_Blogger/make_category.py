import pandas as pd
from datetime import date
import re

file_name = 'yaesul1205-2021-07-09.csv'

nick_name = re.findall('[^-]+-{1}',file_name)[0][:-1]

category_name = ['A','B']
category_list = [('A',['충북','프리다이빙']),('B',['맛집','제주'])]
category_dataframe_list = []
base_df = pd.read_csv(file_name)



for category_ in category_list:
    category_items = category_[1]
    category_name = category_[0]
    category = []
    for item in category_items:
        item_bool = base_df['Title'].apply(lambda x: item in x)
        item_df = base_df[item_bool]
        category.append(item_df)    
    category_dataframe_list.append((category_name,category))

for category,category_dataframe_ in zip(category_list,category_dataframe_list):
    category_dataframe_name = category_dataframe_[0]
    category_dataframe_items = category_dataframe_[1]

    category_input = dict()
    category_item_mulcol = list(category_dataframe_items[0].columns)[1:]*2
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

