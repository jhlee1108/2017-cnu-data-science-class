import fitbit
import json
import configparser
import pandas as pd

config = configparser.RawConfigParser()
config.read('config.ini')

CLIENT_ID = config.get('ACCOUNT', 'CLIENT_ID')
CLIENT_SECRET = config.get('ACCOUNT', 'CLIENT_SECRET')
ACCESS_TOKEN = config.get('ACCOUNT', 'ACCESS_TOKEN')
REFRESH_TOKEN = config.get('ACCOUNT', 'REFRESH_TOKEN')

authd_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET,
                                access_token=ACCESS_TOKEN, 
                                refresh_token=REFRESH_TOKEN)

dates = pd.date_range('20170310', '20170324')

for date in dates:
    intraday_step = authd_client.intraday_time_series('activities/steps',
                                                    base_date=date.strftime('%Y-%m-%d'),
                                                    detail_level='15min')
 
    fname = 'data/' + date.strftime('%Y%m%d') + '_step.json'
    f = open(fname, 'w')
    json.dump(intraday_step, f)

