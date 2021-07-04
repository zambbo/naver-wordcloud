import pandas as pd
from konlpy.tag import Okt
import os
from collections import Counter
from datetime import date
def run():
        
    os.chdir('./coupang/')
    item_file_name = 'Coupang_보석십자수_2021_7_4.csv'
    coupang_df = pd.read_csv(item_file_name)

    review_s = coupang_df['review_list']

    #전체리뷰 깔끔하게 한 str로 만들기.
    review = review_s.str.cat(sep=' ').replace('\\n','').replace(',','').replace('[','').replace(']','').replace('\'','')
    # print(type(review_s))
    # print(review_s[:500])

    okt = Okt()

    review_list = list(map(''.join,zip(*[iter(review)]*1000)))
    print('before noun')
    coupang_nouns = [okt.nouns(review) for review in review_list]
    print('middle noun')
    coupang_noun = []
    for noun in coupang_nouns:
        print('processing...')
        coupang_noun.extend(noun)
    print('after noun')

    print('before count')
    count = Counter(coupang_noun)
    print('after count')
    print(count)
    coupang_frequency_list = count.most_common()

    for i,(key,value) in enumerate(coupang_frequency_list):
        if len(key) <2:
            coupang_frequency_list.pop(i)

    coupang_dict = dict()
    for noun,noun_count in coupang_frequency_list:
        coupang_dict[noun] = noun_count

    coupang_noun_df = pd.DataFrame(coupang_dict,index=['noun_count'])   
    coupang_noun_df.to_csv(f'coupang-frequency-{date.today().isoformat()}.csv')

    print("finish saving")
    
if __name__ == '__main__':
    run()