
# coding: utf-8

# In[1]:


from pyspark.ml.clustering import KMeans
from pyspark.sql.functions import mean
import os
import time
import pandas as pd


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


sleep_min = df_sokulee['sleep'].min()
sleep_max = df_sokulee['sleep'].max()
steps_min = df_sokulee['steps'].min()
steps_max = df_sokulee['steps'].max()
wearing_time_min = df_sokulee['wearing_time'].min()
wearing_time_max = df_sokulee['wearing_time'].max()
print(sleep_min, sleep_max)
print(steps_min, steps_max)
print(wearing_time_min, wearing_time_max)


# In[5]:


df_sokulee['sleep'] = (df_sokulee['sleep'] - sleep_min) / (sleep_max - sleep_min)
df_sokulee['steps'] = (df_sokulee['steps'] - steps_min) / (steps_max - steps_min)
df_sokulee['wearing_time'] = (df_sokulee['wearing_time'] - wearing_time_min) / (wearing_time_max - wearing_time_min)
df_sokulee.head()


# In[6]:


f = open('test.txt', 'w')
lable = 0

for uid in df_sokulee['id']:
    for r in df_sokulee.loc[df_sokulee['id'] == uid].iterrows():
        f.write('{0} 1:{1} 2:{2} 3:{3}\n'.format(lable, r[1][1], r[1][2], r[1][3]))
        lable += 1
f.close()


# In[7]:


dataset = spark.read.format("libsvm")                .load("/home/hadoop/pyspark/test.txt")
dataset.show()


# In[8]:


kmeans = KMeans().setK(4).setSeed(1)
model = kmeans.fit(dataset)


# In[9]:


wssse = model.computeCost(dataset)
print("Within Set Sum of Squared Errors = " + str(wssse))


# In[10]:


centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)

