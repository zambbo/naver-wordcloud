import pandas as pd
from math import log
import re
from konlpy.tag import Okt
from nltk.tokenize import word_tokenize
import numpy as np
from matplotlib import pyplot as plt
from pandas.io.formats.format import DataFrameFormatter

class TfIdf:
    def __init__(self):
        self.stopwords = stopwords = '고 요 은 서 력 하다 에 의 도 더 뭐 저 에 을 랑 로 적 게 제 는 이 있 하 것 들 그 되 수 이 보 않 없 나 사람 주 아니 등 같 우리 때 년 가 한 지 대하 오 말 일 그렇 위하'.split()

    def ad2bin(self,_df):
        _df['AD'] = _df['AD'].fillna(0)
        _df.loc[_df['AD'] != 0,'AD'] = 1
        return _df

    def noad_tfidfdocuments(self,_df):
        print('start!')
        _df = self.ad2bin(_df)
        _df_NOAD = _df[_df['AD'] == 0]
        NOAD_POSTS = _df_NOAD['Post']

        # 본문 list를 모두 전처리( 토큰화,steming)함
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
        noad_df.to_csv('noads.csv')
        print('finish!')

    def noad_tfidf(self,_df,_type=None):
        print('start!')
        _df = self.ad2bin(_df)
        _df_NOAD = _df[_df['AD'] == 0]
        NOAD_POSTS = _df_NOAD['Post']

        print(f"NOAD POSTS NUM : {len(NOAD_POSTS)}")
        # 본문 list를 모두 전처리( 토큰화,steming)함
        NOAD_POSTS  = [self.preprocessingSTR(post) for post in NOAD_POSTS]

        item_dict,bow = self.DTM(NOAD_POSTS)
        key_list = item_dict.keys()

        idf_dict = self.idf_dict(key_list,NOAD_POSTS)

        print(idf_dict)
        tfidf_list = []
        for post in NOAD_POSTS:
            tfidf_list_ = []
            for word in key_list:
                if _type is 'one':
                    tfidf_list_.append(self.tfidf_dict_one(word,post,idf_dict))
                else:
                    tfidf_list_.append(self.tfidf_dict(word,post,idf_dict))
            tfidf_list.append(tfidf_list_)
            



        for index,tfidfs in enumerate(tfidf_list):
            tfidf_list[index] = self.normalize(tfidfs)

        noad_df = pd.DataFrame(data=tfidf_list,columns=key_list)
        if _type is 'one':
            noad_df.to_csv('noad-one.csv')
        else:
            noad_df.to_csv('noad.csv')
        self.noad_df = noad_df
        print('finish!')
            
    def ad_tfidfdocuments(self,_df):
        print('start!')
        _df = self.ad2bin(_df)
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
        ad_df.to_csv('ads.csv')
        print('finish!')

    def ad_tfidf(self,_df,_type=None):
        print('start!')
        _df = self.ad2bin(_df)
        df_AD = _df[_df['AD'] == 1]
        AD_POSTS = df_AD['Post']
        AD_POSTS = [self.preprocessingSTR(post) for post in AD_POSTS]
            
        item_dict,bow = self.DTM(AD_POSTS)

        key_list = item_dict.keys()

        idf_dict = self.idf_dict(key_list,AD_POSTS)

        print(idf_dict)
        tfidf_list = []
        for post in AD_POSTS:
            tfidf_list_ = []
            for word in key_list:
                if _type is 'one':
                    tfidf_list_.append(self.tfidf_dict_one(word,post,idf_dict))
                else:
                    tfidf_list_.append(self.tfidf_dict(word,post,idf_dict))
            tfidf_list.append(tfidf_list_)
            

        for index,tfidfs in enumerate(tfidf_list):
            tfidf_list[index] = self.normalize(tfidfs)

        ad_df = pd.DataFrame(data=tfidf_list,columns=key_list)
        if _type is 'one':
            ad_df.to_csv('ad-one.csv')
        else:
            ad_df.to_csv('ad.csv')

        self.ad_df = ad_df
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

    def tf1d_one(self,t,d):
        return int(t in d)

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

    def idf_dict(self,t_list,docs):
        idf_dict = dict()
        for t in t_list:
            t_idf = self.idf(t,docs)
            idf_dict[t] = t_idf
        return idf_dict

    def tfidf(self,t,d,docs):
        return self.tf1d(t,d)*self.idf(t,docs)

    def tfidf_dict(self,t,d,idf_dict):
        return self.tf1d(t,d)*idf_dict[t]
    
    def tfidf_dict_one(self,t,d,idf_dict):
        return self.tf1d_one(t,d)*idf_dict[t]

    def tfidfdocuments(self,t, docs):
        return self.tfdocuments(t,docs)*self.idf(t,docs)

    def normalize(self, _num_list):
        denominator = np.max(_num_list) - np.min(_num_list)
        _num_list = np.array(_num_list)
        _num_list = _num_list - np.min(_num_list)
        _num_list = _num_list/denominator
        return _num_list

    def TopNMeanTfIdf(self,top_n=5,type=None):
        if type is None:
            return
        elif type is 'AD':
            df = self.ad_df
        elif type is 'NOAD':
            df = self.noad_df
        
        df = df.drop('Unnamed: 0',axis=1)
        mean = df.mean(axis=0)
        return mean.sort_values(ascending=False)[:top_n]

    def plotTopNMeanTfIdf(self,top_n = 5,type=None):
        if type is None:
            return
        elif type is 'AD':
            AD_df = self.ad_df
        elif type is 'NOAD':
            NOAD_df = self.noad_df
        
        

def run():
    df = pd.read_csv('./data/bosuk.csv')

    tfidf = TfIdf()
    tfidf.noad_tfidf(df)
    tfidf.ad_tfidf(df)

    
if __name__ =='__main__':
    run()