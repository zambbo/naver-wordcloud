import pandas as pd
import numpy as np
df = pd.read_csv('ad.csv')
df = df.drop('Unnamed: 0',axis=1)
mean = df.mean(axis=0)
mean.sort_values(ascending=False)[:30]