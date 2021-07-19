import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
font_location = r'C:\Windows\Fonts\SeoulNamsanB.ttf'
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font',family=font_name)
file_name = 'ad.csv'

df = pd.read_csv(file_name)
df.drop('Unnamed: 0',axis=1,inplace=True)


def TopNMeanTfIdf(_df,top_n=5):
    mean = df.mean(axis=0)
    return mean.sort_values(ascending=False)[:top_n]

def plot2DScatter(_df):
    Top5 = TopNMeanTfIdf(_df,5)

    
    for key in Top5.keys():
        label = key
        X = _df[key].keys()
        y = _df[key].values
        print(label,X,y)
        plt.scatter(X,y,label = label)
    plt.legend()
    plt.show()

plot2DScatter(df) 
# toptfidf = TopNMeanTfIdf(df,50)
# toptfidf.values
# plt.bar(toptfidf.keys(),toptfidf.values)
# plt.show()