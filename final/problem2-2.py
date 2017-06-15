
# coding: utf-8

# In[1]:


import os
import time
import pandas as pd
from pyspark.sql.functions import sum


# In[2]:


st=time.time()
directory_path = '/home/hadoop/pyspark/sokulee/'
f = open('sokulee_sum.csv', 'w')
f.write('id,sleep,steps,wearing_time\n')
for n in range(1,100):
    name = 'A0' + str(n)
    directory_name = directory_path + name

    if os.path.exists(directory_name):
        df_sleep_temp = spark.read.json(directory_name + '/*_sleep.json')
        df_steps_temp = spark.read.json(directory_name + '/*_steps.json')
        df_heart_temp = spark.read.json(directory_name + '/*_heart.json')

        a = df_sleep_temp.select(sum(df_sleep_temp['summary']['totalTimeInBed']).alias('sleep'))
        b = df_steps_temp.select(sum(df_steps_temp['activities-steps'][0]['value']).alias('steps'))
        c = df_heart_temp.select(sum(df_heart_temp['activities-heart'][0]['value']['heartRateZones'][0]['minutes'] 
                    + df_heart_temp['activities-heart'][0]['value']['heartRateZones'][1]['minutes'] 
                    + df_heart_temp['activities-heart'][0]['value']['heartRateZones'][2]['minutes'] 
                    + df_heart_temp['activities-heart'][0]['value']['heartRateZones'][3]['minutes']).alias('time'))
        
        f.write(name + ',' + str(a.collect()[0][0]) + ',' + str(b.collect()[0][0]) + ',' + str(c.collect()[0][0]) + '\n')
        
f.close()
print(time.time()-st, 'sec')


# In[7]:


df_sokulee = pd.read_csv('sokulee_sum.csv')
df_sokulee.head()


# In[13]:


df_sokulee['steps'].sort_values(ascending=False)[:5]


# In[14]:


df_sokulee['sleep'].sort_values(ascending=False)[:5]


# In[15]:


df_sokulee['wearing_time'].sort_values(ascending=False)[:5]

