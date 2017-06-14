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
name = 'A0100'
for date in dates:
    x = datetime.datetime.strptime(date.strftime('%Y-%m-%d'), '%Y-%m-%d')
    intraday_sleep = authd_client.get_sleep(x)
    fname = 'data/' + name + '_' + date.strftime('%Y%m%d') + '_sleep.json'
    f = open(fname, 'w')
    json.dump(intraday_sleep, f)
