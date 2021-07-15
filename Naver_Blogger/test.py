# filename = './csvfile/보석십자수2021-07-06.csv'

# import pandas as pd
# import re
# df = pd.read_csv(filename)
# urls = df['Post URL']
# urls = urls.apply(lambda x: re.findall("com\/.*\?",x))[0][4:-1]
# urls = [re.findall('com\/.*\?',x)[0][4:-1] for x in urls]
# urls

# import pandas as pd

# file_name = './temp_csv/306_1203-2021-07-15.csv'
# df = pd.read_csv(file_name)
# link_list = df['Link'].tolist()
# title_list = df['Title'].tolist()

# link_title_list = [(link,title) for link,title in zip(link_list,title_list)]
# link_title_list