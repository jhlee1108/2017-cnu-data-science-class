import pandas as pd
import matplotlib.pyplot as plt

def compare_tashu_station_by_gu():
    station = pd.read_csv('station.csv')
    station_count_by_gu = station.groupby('구별').구별.count()
    plt.title('Compare tashu station by gu')
    station_count_by_gu.plot(kind='bar');
    plt.show()

def compare_usage_rate_by_gu():
    tashu = pd.read_csv('tashu.csv')
    station = pd.read_csv('tashu.csv')


if __name__ == '__main__':
    compare_tashu_station_by_gu()
