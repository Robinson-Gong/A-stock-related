import pandas as pd
import numpy as np

df = pd.read_excel(r'C:\Users\Administrator\Desktop\data\债券\新期限结构.xlsx')
rate_list = []
for i in range(df.shape[0]):
    rate_list.append[df.loc[i,'主体评级']]
