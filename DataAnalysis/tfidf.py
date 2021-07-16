import pandas as pd
from math import log
import re
from konlpy.tag import Okt
from nltk.tokenize import word_tokenize
import numpy as np

class TfIdf:
    def __init__(self):
        self.stopwords = stopwords = '고 요 은 서 력 하다 에 의 도 더 뭐 저 에 을 랑 로 적 게 제 는 이 있 하 것 들 그 되 수 이 보 않 없 나 사람 주 아니 등 같 우리 때 년 가 한 지 대하 오 말 일 그렇 위하'.split()

    def noad_tfidf(self,_df):
        print('start!')
        _df['AD'] = _df['AD'].fillna(0)
        _df.loc[_df['AD'] != 0,'AD'] = 1
        _df_NOAD = _df[_df['AD'] == 0]
        NOAD_POSTS = _df_NOAD['Post']
        NOAD_POSTS  = [self.preprocessingSTR(post) for post in NOAD_POSTS]

        item_dict,bow = self.DTM(NOAD_POSTS)
        tfidf_list = []
        for word in item_dict.keys():
            tfidf_list.append(self.tfidf(word,NOAD_POSTS))

        key_list = item_dict.keys()


        tfidf_list = self.normalize(tfidf_list)
        NOAD_DATA = []
        for key,tfidf in zip(key_list,tfidf_list):
            NOAD_DATA.append((key,tfidf))
        noad_df = pd.DataFrame(NOAD_DATA)
        noad_df.to_csv('noad.csv')
        print('finish!')
    def ad_tfidf(self,_df):
        print('start!')
        _df['AD'] = _df['AD'].fillna(0)
        _df.loc[_df['AD'] != 0,'AD'] = 1
        df_AD = _df[_df['AD'] == 1]
        AD_POSTS = df_AD['Post']
        AD_POSTS = [self.preprocessingSTR(post) for post in AD_POSTS]
            
        item_dict,bow = self.DTM(AD_POSTS)
        tfidf_list = []
        for word in item_dict.keys():
            tfidf_list.append(self.tfidf(word,AD_POSTS))

        key_list = item_dict.keys()


        tfidf_list = self.normalize(tfidf_list)
        AD_DATA = []
        for key,tfidf in zip(key_list,tfidf_list):
            AD_DATA.append((key,tfidf))
        ad_df = pd.DataFrame(AD_DATA)
        ad_df.to_csv('ad.csv')
        print('finish!')
    #전처리해주는 과정.
    def preprocessingSTR(self,_str):
        okt = Okt()
        _str = re.sub('[^가-힣 ]','',_str)
        morphs = okt.morphs(_str,stem=True)
        morphs = [text for text in morphs if text not in self.stopwords]
        morphs = [text for text in morphs if len(text) >1]
        return morphs
    


    def DTM(self,documents):
        items = dict()
        bow = []
        for doc in documents:
            for word in doc:
                #만약 아직 사전에 없는 단어라면
                if items.get(word) is None:
                    #item의 index를 추가해줌.
                    items[word] = len(items.keys())

                    bow.append(1)

                else:
                    index = items[word]

                    bow[index] = bow[index] + 1
        
        return items,bow

    def tf1d(self,t,d):
        return d.count(t)

    def tfdocuments(self,t,docs):
        word_count = 0
        for doc in docs:
            word_count +=t in doc
        return word_count

    def tflistsdocuments(self,ts,docs):
        ts = [self.tfdocuments(t,docs) for t in ts]
        return ts
        
    def idf(self,t,docs):
        df = 0
        for doc in docs:
            df += t in doc
        return float(log(len(docs) / (1+df)))


    def tfidf(self,t, docs):
        return self.tfdocuments(t,docs)*self.idf(t,docs)

    def normalize(self,_num_list):
        denominator = np.max(_num_list) - np.min(_num_list)
        _num_list = np.array(_num_list)
        _num_list = _num_list - np.min(_num_list)
        _num_list = _num_list/denominator
        return _num_list

def run():
    df = pd.read_csv('./data/bosuk.csv')

    tfidf = TfIdf()
    tfidf.ad_tfidf(df)
    tfidf.noad_tfidf(df)
    
if __name__ =='__main__':
    run()