from wordcloud import WordCloud
from extract_noun_frequency import df2nounList
import pandas as pd


csv_file_name = 'noun_bosuk10-haruclass.csv'

font_path = r'C:\Windows\Fonts\SeoulNamsanB.ttf'


df = pd.read_csv(csv_file_name)

noun_dict = dict(df2nounList(df))

wc = WordCloud(font_path=font_path,
background_color='white',
colormap='Accent_r',
width = 800,
height=600)

wc = wc.generate_from_frequencies(noun_dict)


#wc.to_file('haru.png')


