
# coding: utf-8

# In[1]:

import pandas as pd
import datetime
import time


# In[2]:

df_tashu = pd.read_csv('../data/tashu.csv')
df_tashu


# In[3]:

st=time.time()
df_tashu['RENT_DATE'] = df_tashu['RENT_DATE']                        .apply(lambda x: datetime.datetime                               .strptime(str(x), '%Y%m%d%H%M%S'))
print(time.time()-st, 'sec')
df_tashu


# In[4]:

df_tashu['WEEKDAY'] = df_tashu['RENT_DATE'].dt.dayofweek
df_tashu


# In[58]:

df_rent = pd.DataFrame()
for i in range(0,7):
    df_rent[i] = df_tashu.loc[df_tashu['WEEKDAY'] == i].groupby('RENT_STATION').count()['RENT_DATE']
df_rent


# In[41]:

df_rent_weekday = df_rent.ix[:,[0,1,2,3,4]]
df_rent_weekday


# In[56]:

df_rent_weekday.fillna(0).astype(int).sum(axis=1).sort_values(ascending=False)[:5]


# In[40]:

df_rent_weekend = df_rent.ix[:,[5,6]]
df_rent_weekend


# In[57]:

df_rent_weekend.fillna(0).astype(int).sum(axis=1).sort_values(ascending=False)[:5]

