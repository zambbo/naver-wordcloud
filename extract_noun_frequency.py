from konlpy.tag import Okt
from collections import Counter
import pandas as pd
from datetime import date

#csv_file_list = ['arduino-mechasolution.csv','bosuk10-haruclass.csv','bosuk10-limenamu.csv']
csv_file_list = ['0-2021-07-04.csv','1-2021-07-04.csv','2-2021-07-04.csv','3-2021-07-04.csv','4-2021-07-04.csv','5-2021-07-04.csv','6-2021-07-04.csv']

def readCSVFromName(_csv_file_name=None):
    try:
        df = pd.read_csv(_csv_file_name)
    except:
        return None
    return df
    
def df2nounList(_df):
    sr = _df.iloc[0]
    noun_list = list(zip(sr.index,sr.values))
    noun_list.pop(0)
    return noun_list

def getNouns(_str):
    okt = Okt()
    print('NounStart!')
    nouns = okt.nouns(_str)
    nouns = [noun for noun in nouns if len(noun)>1]
    print('NounFinish!')
    return nouns

def makeStrWithDf(_df,_columnname):
    str_list = list(_df[_columnname])
    return ' '.join(str_list)

def getMost100CountFromStr(_str):
    count = Counter(_str)
    noun_list = count.most_common(100)
    return noun_list

def getAllCountFromStr(_str):
    count = Counter(_str)
    noun_list = count.most_common()
    return noun_list

def getAllCountFromStrs(_str_list):
    count_list = [Counter(_str) for _str in _str_list]
    count_sum = sum(count_list,Counter())
    return count_sum.most_common()

def getMost100CountFromStrs(_str_list):
    count_list = [Counter(_str) for _str in _str_list]
    count_sum = sum(count_list,Counter())
    return count_sum.most_common(100)

def readCSVFromFileList(_file_list):
    df_list = [readCSVFromName(file_name) for file_name in _file_list]
    return df_list

def storeNounListCSVFromFiles(_csv_file_list):
    # csv파일이름list로부터 DataFrame list 생성
    df_list = readCSVFromFileList(_csv_file_list)

    # DataFrame list로부터 review말뭉치 list 생성
    review_list = [makeStrWithDf(df,'reviewContent') for df in df_list]

    # 말뭉치 list로부터 명사 추출한 list의 list 생성
    noun_list = [getNouns(review) for review in review_list]

    # 명사추출 list의 list로부터 전체 명사당 빈도수 list 생성
    noun_frequency_list = getAllCountFromStrs(noun_list)

    noun_dict = dict()
    for noun,noun_count in noun_frequency_list:
        noun_dict[noun] = noun_count

    noun_df = pd.DataFrame(noun_dict,index=['noun_count'])
    noun_df.to_csv(f'noun_frquency-{date.today().isoformat()}.csv')

# def storeNounListCSVFromFileName(_csv_file_name):

#     df = readCSVFromName(_csv_file_name)

#     #OKT 명사 추출을 위해서 하나의 거대한 문자열 만들기.
#     review = makeStrWithDf(df,'reviewContent')
#     nouns = getNouns(review)
#     #noun_list = getMost100CountFromStr(nouns)
#     noun_list = getAllCountFromStr(nouns)

#     noun_dict = dict()
#     for noun,noun_count in noun_list:
#         noun_dict[noun] = noun_count

#     noun_df = pd.DataFrame(noun_dict,index=['noun_count'])
#     noun_df.to_csv('Allnoun_' + _csv_file_name)

def main():
    storeNounListCSVFromFiles(csv_file_list)

if __name__ == '__main__':
    main()