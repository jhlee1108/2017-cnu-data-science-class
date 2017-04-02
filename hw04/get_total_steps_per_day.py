import os
import pandas as pd
import json

dates = pd.date_range('20160401', '20160520').strftime('%Y%m%d')
directory_path = 'sokulee/'
f = open('steps.csv' ,'w')

f.write('name')
for date in dates:
    f.write(',' + date)
f.write('\n')

for n in range(1,100):
    name = 'A0' + str(n)
    directory_name = directory_path + name
    
    if os.path.exists(directory_name):
        f.write(name)
        for date in dates:
            f_steps_path = directory_name + '/' + name + '_' + date + '_steps.json'
            try : f_steps = open(f_steps_path)
            except IOError as e:
                print(e)
                f.write(',0')
            else:
                data_steps = json.loads(f_steps.read())
                try : f.write(',' + str(data_steps['activities-steps'][0]['value']))
                except KeyError as e:
                    print(e)
                    f.write(',0')
        f.write('\n')

f.close()
