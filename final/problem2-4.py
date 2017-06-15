
# coding: utf-8

# In[1]:


import os
import time
import pandas as pd
from pyspark.sql.functions import mean


# In[2]:


st=time.time()
directory_path = '/home/hadoop/pyspark/sokulee/'
f = open('sokulee.csv', 'w')
f.write('id,sleep,steps,wearing_time\n')
for n in range(1,100):
    name = 'A0' + str(n)
    directory_name = directory_path + name

    if os.path.exists(directory_name):
        df_sleep_temp = spark.read.json(directory_name + '/*_sleep.json')
        df_steps_temp = spark.read.json(directory_name + '/*_steps.json')
        df_heart_temp = spark.read.json(directory_name + '/*_heart.json')

        a = df_sleep_temp.select(mean(df_sleep_temp['summary']['totalTimeInBed']).alias('sleep'))
        b = df_steps_temp.select(mean(df_steps_temp['activities-steps'][0]['value']).alias('steps'))
        c = df_heart_temp.select(mean(df_heart_temp['activities-heart'][0]['value']['heartRateZones'][0]['minutes'] 
                    + df_heart_temp['activities-heart'][0]['value']['heartRateZones'][1]['minutes'] 
                    + df_heart_temp['activities-heart'][0]['value']['heartRateZones'][2]['minutes'] 
                    + df_heart_temp['activities-heart'][0]['value']['heartRateZones'][3]['minutes']).alias('time'))
        
        f.write(name + ',' + str(a.collect()[0][0]) + ',' + str(b.collect()[0][0]) + ',' + str(c.collect()[0][0]) + '\n')
        
f.close()
print(time.time()-st, 'sec')


# In[3]:


df_sokulee = pd.read_csv('sokulee.csv')
df_sokulee.head()


# In[4]:


import math
from operator import itemgetter
from scipy.spatial import distance

def distance_euclidean(a, b):
    return 1/(distance.euclidean(a,b)+1)


# In[5]:


def nearest_neighbor_user(user, topN, simFunc):
    nn = {}
    interSectionU1 = []
    for r in df_sokulee.loc[df_sokulee['id'] == user].iterrows():
        interSectionU1.append(r[1][1])
        interSectionU1.append(r[1][2])
        interSectionU1.append(r[1][3])
    
    ## Brote Force Compute
    for uid in df_sokulee['id']:
        interSectionU2 = []
        
        if uid == user:
            continue
        
        for r in df_sokulee.loc[df_sokulee['id'] == uid].iterrows():
            interSectionU2.append(r[1][1])
            interSectionU2.append(r[1][2])
            interSectionU2.append(r[1][3])
            
        ## similarity function
        sim = simFunc(interSectionU1, interSectionU2)
        
        if math.isnan(sim) == False:
            nn[uid] = sim
            
    ## top N returned
    return sorted(nn.items(), key=itemgetter(1))[:-(topN+1):-1]


# In[6]:


sleep_min = df_sokulee['sleep'].min()
sleep_max = df_sokulee['sleep'].max()
steps_min = df_sokulee['steps'].min()
steps_max = df_sokulee['steps'].max()
wearing_time_min = df_sokulee['wearing_time'].min()
wearing_time_max = df_sokulee['wearing_time'].max()
print(sleep_min, sleep_max)
print(steps_min, steps_max)
print(wearing_time_min, wearing_time_max)


# In[7]:


df_sokulee['sleep'] = (df_sokulee['sleep'] - sleep_min) / (sleep_max - sleep_min)
df_sokulee['steps'] = (df_sokulee['steps'] - steps_min) / (steps_max - steps_min)
df_sokulee['wearing_time'] = (df_sokulee['wearing_time'] - wearing_time_min) / (wearing_time_max - wearing_time_min)
df_sokulee.head()


# In[8]:


neighbor = nearest_neighbor_user('A08', 10, distance_euclidean)
for n in neighbor:
    print(n)


# In[9]:


neighbor = nearest_neighbor_user('A08', 1, distance_euclidean)
for n in neighbor:
    print(n)

