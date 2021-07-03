from konlpy.tag import Okt
from collections import Counter
import pandas as pd

csv_file_list = ['arduino-mechasolution.csv','bosuk10-haruclass.csv','bosuk10-limenamu.csv']


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

def storeNounListCSVFromFileName(_csv_file_name):

    df = readCSVFromName(_csv_file_name)

    #OKT 명사 추출을 위해서 하나의 거대한 문자열 만들기.
    review = makeStrWithDf(df,'reviewContent')
    nouns = getNouns(review)
    noun_list = getMost100CountFromStr(nouns)
    

    noun_dict = dict()
    for noun,noun_count in noun_list:
        noun_dict[noun] = noun_count

    noun_df = pd.DataFrame(noun_dict,index=['noun_count'])
    noun_df.to_csv('noun_' + _csv_file_name)

def main():
    for filename in csv_file_list:
        storeNounListCSVFromFileName(filename)

if __name__ == '__main__':
    main()