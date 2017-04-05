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
                json_sleep = json.loads(f_sleep.read())
                try: 
                    data_sleep = json_sleep['sleep']
                except KeyError as e:
                    print(str(e))
                except IndexError as e:
                    print(str(e))
                else:
                    prev_time_to_wake_up = -10 # init prev_time_to_wake_up
                    for t in data_sleep:
                        time_to_sleep = int(t['minuteData'][0]['dateTime'][:2])
                        time_to_wake_up = int(t['minuteData'][-1]['dateTime'][:2])

                        if time_to_sleep <= 10:
                            time_to_sleep += 24

                        if time_to_sleep - prev_time_to_wake_up <= 2:
                            end_sleep[len(end_sleep)-1] = time_to_wake_up
                        else:
                            start_sleep.append(time_to_sleep)
                            end_sleep.append(time_to_wake_up)

                        prev_time_to_wake_up = time_to_wake_up

        mean_time_to_sleep = sum(start_sleep)/len(start_sleep)
        mean_time_to_wake_up = sum(end_sleep)/len(end_sleep)
        if mean_time_to_sleep >= 24:
            mean_time_to_sleep -= 24
        start_sleep_mean.append(mean_time_to_sleep)
        end_sleep_mean.append(mean_time_to_wake_up)

df['start'] = start_sleep_mean
df['end'] = end_sleep_mean
df.index = names
df.to_csv('sleep.csv')
