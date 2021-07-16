from wordcloud import WordCloud
import pandas as pd


csv_file_name = 'noad.csv'

font_path = r'C:\Windows\Fonts\SeoulNamsanB.ttf'


df = pd.read_csv(csv_file_name)
words = df['0'].tolist()
tfidf = df['1'].tolist()
datas = dict()
for word,tfidf in zip(words,tfidf):
    if tfidf != 0:
        datas[word] = tfidf

wc = WordCloud(font_path=font_path,
background_color='white',
colormap='Accent_r',
width = 800,
height=600)

wc = wc.generate_from_frequencies(datas)



#wc.to_file('haru.png')
