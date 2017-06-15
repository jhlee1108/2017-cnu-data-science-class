
# coding: utf-8

# In[31]:

import pandas as pd
import os
import json


# In[32]:

directory_path = '../data/sokulee/'


# In[33]:

dates = pd.date_range('20160401', '20160520').strftime('%Y%m%d')


# In[34]:

df_steps = pd.DataFrame(index=dates)


# In[35]:

for n in range(1,100):
    name = 'A0' + str(n)
    directory_name = directory_path + name
    total_steps = list()

    if os.path.exists(directory_name):
        for date in dates:
            f_steps_path = directory_name + '/' + name + '_' + date + '_steps.json'

            try : 
                f_steps = open(f_steps_path)
            except IOError as e:
                total_steps.append(0)
            else:
                data_steps = json.loads(f_steps.read())

                try :
                    total_steps.append(int(data_steps['activities-steps'][0]['value']))
                except KeyError as e:
                    total_steps.append(0)

        df_steps[name] = total_steps
df_steps.head()


# In[36]:

df_total_steps = pd.DataFrame(data=df_steps.sum(axis=0), index=df_steps.columns, columns=['total_steps'])
df_total_steps.head()


# In[37]:

df_total_steps.sort_values(by=['total_steps'], inplace=True, ascending=False)
df_total_steps.head()


# In[38]:

top5_steps = df_total_steps[:5]
top5_steps


# In[39]:

df_sleep = pd.DataFrame(index=dates)


# In[40]:

for n in range(1,100):
    name = 'A0' + str(n)
    directory_name = directory_path + name
    total_steps = list()

    if os.path.exists(directory_name):
        for date in dates:
            f_steps_path = directory_name + '/' + name + '_' + date + '_sleep.json'

            try : 
                f_steps = open(f_steps_path)
            except IOError as e:
                total_steps.append(0)
            else:
                data_steps = json.loads(f_steps.read())

                try :
                    total_steps.append(int(data_steps['summary']['totalTimeInBed']))
                except KeyError as e:
                    total_steps.append(0)

        df_sleep[name] = total_steps
df_sleep.head()


# In[41]:

df_total_sleep = pd.DataFrame(data=df_sleep.sum(axis=0), index=df_sleep.columns, columns=['total_sleep'])
df_total_sleep.head()


# In[42]:

df_total_sleep.sort_values(by=['total_sleep'], inplace=True, ascending=False)
df_total_sleep.head()


# In[43]:

top5_sleep = df_total_sleep[:5]
top5_sleep


# In[44]:

df_wear = pd.DataFrame(index=dates)


# In[45]:

for n in range(1,100):
    name = 'A0' + str(n)
    directory_name = directory_path + name
    wearing = pd.Series(index=dates)

    if os.path.exists(directory_name):
        for date in dates:
            f_heart_path = directory_name + '/' + name + '_' + date + '_heart.json'
            
            try : 
                f_heart = open(f_heart_path)
            except IOError as e:
                print('file not exist')
            else:
                data_heart = json.loads(f_heart.read())
                wearing_time = 0
                for i in range(0, 4):
                    try :
                        minutes = data_heart['activities-heart'][0]['value']['heartRateZones'][i]['minutes']
                    except KeyError as e:
                        print('key error')
                    else:
                        wearing_time += minutes
            wearing.loc[date] = wearing_time
            
        df_wear[name] = wearing.astype(int)
df_wear.head()


# In[46]:

df_total_wear = pd.DataFrame(data=df_wear.sum(axis=0), index=df_wear.columns, columns=['total_wear'])
df_total_wear.head()


# In[47]:

df_total_wear.sort_values(by=['total_wear'], inplace=True, ascending=False)
df_total_wear.head()


# In[48]:

top5_wear = df_total_wear[:5]
top5_wear

