import os
import pandas as pd
import json

dates = pd.date_range('20160401', '20160520')
directory_path = 'sokulee/'
df = pd.DataFrame()
names = list()
start_sleep_mean = list()
end_sleep_mean = list()

for n in range(1,100):
    name = 'A0' + str(n)
    directory_name = directory_path + name
    start_sleep = list()
    end_sleep = list()

    if os.path.exists(directory_name):
        names.append(name)

        for date in dates:
            f_sleep_path = directory_name + '/' + name + '_'\
                            + date.strftime('%Y%m%d') + '_sleep.json'

            try: 
                f_sleep = open(f_sleep_path)
            except IOError as e:
                print(str(e))
            else:
                data_sleep = json.loads(f_sleep.read())

                try: 
                    time_sleep = data_sleep['sleep'][0]['minuteData']
                except KeyError as e:
                    print(str(e))
                except IndexError as e:
                    print(str(e))
                else:
                    start_sleep.append(int(time_sleep[0]['dateTime'][:2]))
                    end_sleep.append(int(time_sleep[-1]['dateTime'][:2]))

        start_sleep_mean.append(sum(start_sleep)/len(start_sleep))
        end_sleep_mean.append(sum(end_sleep)/len(end_sleep))

df['start'] = start_sleep_mean
df['end'] = end_sleep_mean
df.index = names
df.to_csv('sleep.csv')
