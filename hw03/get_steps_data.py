import fitbit
import json
import configparser
import pandas as pd
import datetime

config = configparser.RawConfigParser()
config.read('config.ini')

CLIENT_ID = config.get('ACCOUNT', 'CLIENT_ID')
CLIENT_SECRET = config.get('ACCOUNT', 'CLIENT_SECRET')
ACCESS_TOKEN = config.get('ACCOUNT', 'ACCESS_TOKEN')
REFRESH_TOKEN = config.get('ACCOUNT', 'REFRESH_TOKEN')

authd_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET,
                                access_token=ACCESS_TOKEN, 
                                refresh_token=REFRESH_TOKEN)

dates = pd.date_range('20170401', '20170520')

for date in dates:
    intraday_steps = authd_client\
                    .intraday_time_series('activities/steps', 
                            base_date=date.strftime('%Y-%m-%d'), 
                            detail_level='1min')
    fname = 'data/' + date.strftime('%Y%m%d') + '_steps.json'
    f = open(fname, 'w')
    json.dump(intraday_steps, f)
