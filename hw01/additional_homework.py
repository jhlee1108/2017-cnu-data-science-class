import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def compare_tashu_station_by_gu():
    station = pd.read_csv('station.csv')
    station_count_by_gu = station.groupby('GU').GU.count()
    plt.title('Compare tashu station by gu')
    station_count_by_gu.plot(kind='bar');
    plt.show()

def compare_usage_rate_by_gu():
    tashu = pd.read_csv('tashu.csv')
    station = pd.read_csv('station.csv')

    rent_station_count = tashu.groupby('RENT_STATION').RENT_STATION.count()
    return_station_count = tashu.groupby('RETURN_STATION').RETURN_STATION.count()
    
    sum_station_count = rent_station_count.add(return_station_count, fill_value=0).astype(int)
    station_number = sum_station_count.index

    station_gu = pd.Series(
        list(station['GU']),
        index=list(station['NUMBER'])
    )

    usage_rate = dict()
    for i in range(1, len(sum_station_count)):
        if station_number[i] in station_gu:
            key = station_gu[station_number[i]]
            value = int(sum_station_count[i])
        else:
            continue

        if key in usage_rate:
            usage_rate[key] = usage_rate[key] + value
        else:
            usage_rate[key] = value

    plt.title('Compare tashu usage rate by gu')
    plt.bar(range(len(usage_rate)), usage_rate.values(), align='center')
    plt.xticks(range(len(usage_rate)), usage_rate.keys())
    plt.show()

def compare_usage_rate_by_day():
    tashu = pd.read_csv('tashu.csv', parse_dates=[1,3])
    tashu['RENT_WEEKDAY'] = pd.DatetimeIndex(tashu['RENT_DATE']).weekday

    rent_weekday = tashu.groupby('RENT_WEEKDAY').RENT_STATION.count()
    plt.title('Compare tashu usage rate by day')
    plt.xticks((0, 1, 2, 3, 4, 5, 6), ('Mon', 'Thu', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun'))
    rent_weekday.plot(kind='bar')
    plt.show()

if __name__ == '__main__':
    matplotlib.rc('font', family='NanumBarunGothic')
    compare_usage_rate_by_day()
