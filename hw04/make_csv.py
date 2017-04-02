import os
import pandas as pd
import json

dates = pd.date_range('20160401', '20160520')
directory_path = 'sokulee/'

for n in range(1,100):
    name = 'A0' + str(n)
    directory_name = directory_path + name

    if os.path.exists(directory_name):
        for date in dates:
            f_heart_path = directory_name + '/' + name + '_'\
                            + date.strftime('%Y%m%d') + '_heart.json'
            try : f_heart = open(f_heart_path)
            except IOError as e:
                print(str(e))
            else:
                data_heart = json.loads(f_heart.read())

            f_sleep_path = directory_name + '/' + name + '_'\
                            + date.strftime('%Y%m%d') + '_sleep.json'
            try : f_sleep = open(f_sleep_path)
            except IOError as e:
                print(str(e))
            else:
                data_sleep = json.loads(f_sleep.read())
        
            f_steps_path = directory_name + '/' + name + '_'\
                            + date.strftime('%Y%m%d') + '_steps.json'
            try : f_steps = open(f_steps_path)
            except IOError as e:
                print(str(e))
            else:
                data_steps = json.loads(f_steps.read())
                try:a = data_steps['activities-steps-intraday']['dataset']
                except KeyError as e:
                    print(e)
                else:
                    for i in a:
                        print(i['time'], i['value'])
        
