import pandas as pd
import json

dates = pd.date_range('20170310', '20170324')
df = pd.DataFrame()

for date in dates:
    fname = 'data/' + date.strftime('%Y%m%d') + '_step.json'
    f = open(fname)
    time = list()
    value = list()

    json_data = json.loads(f.read())
    date_time = json_data['activities-steps'][0]['dateTime']
    data_set = json_data['activities-steps-intraday']['dataset']

    for data in data_set:
        time.append(data['time'])
        value.append(data['value'])

    df[date_time] = value

df.index = time
print(df.head())
