import pandas as pd
import json
import matplotlib
import matplotlib.pyplot as plt

def show_fitbit_steps():
    dates = pd.date_range('20170310', '20170324')
    df_step_per_min = pd.DataFrame()
    step_per_day = list()

    for date in dates:
        fname = 'data/' + date.strftime('%Y%m%d') + '_step.json'
        f = open(fname)
        time = list()
        value = list()

        json_data = json.loads(f.read())
        date_time = json_data['activities-steps'][0]['dateTime']
        data_set = json_data['activities-steps-intraday']['dataset']
        step_per_day.append(int(json_data['activities-steps'][0]['value']))
        f.close()

        for data in data_set:
            time.append(data['time'])
            value.append(data['value'])

        df_step_per_min[date_time] = value

    df_step_per_min.index = time
    df_step_per_min['mean'] = df_step_per_min.mean(axis=1).astype(int)

    df_step_per_day = pd.DataFrame(step_per_day, index=dates, columns=['step'])

    df_step_per_min.plot(y='mean', subplots=True, title='Mean step per minute')
    df_step_per_day.plot(subplots=True, title='Step per day')
    plt.show()

if __name__ == '__main__':
    show_fitbit_steps()    
