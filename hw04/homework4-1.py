import os
import pandas as pd
import json

dates = pd.date_range('20160401', '20160520').strftime('%Y%m%d')
directory_path = 'sokulee/'
df = pd.DataFrame(index=dates)

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
                print(e)
            else:
                data_steps = json.loads(f_steps.read())

                try :
                    total_steps.append(data_steps['activities-steps'][0]['value'])
                except KeyError as e:
                    total_steps.append(0)
                    print(e)

        df[name] = total_steps

df.to_csv('steps.csv')
