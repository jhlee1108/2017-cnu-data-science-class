import csv
from operator import itemgetter
import pandas as pd

def get_top10_station(tashu_dict, station_dict):
    """
    [역할]
    정류장 Top10 출력하기
    대여 정류장과 반납정류장을 합한 총 사용빈도수 Top10

    [입력]
    tashu_dict : csv.DictReader 형태의 타슈대여정보
    station_dict : csv.DictReader 형태의 정류장 정보

    [출력]
    Top10 정류장 리스트
    ex.) [[정류장 이름1, 정류장 번호1, 정류장1 count], [정류장 이름2, 정류장 번호2, 정류장2 count], .....] 형태
    """

    tashu_frame = pd.DataFrame(list(tashu_dict))
    station_frame = pd.DataFrame(list(station_dict))

    station_name = pd.Series(
        list(station_frame['NAME']), 
        index=list(station_frame['NUMBER'])
    )

    rent_station_count = tashu_frame.groupby('RENT_STATION').RENT_STATION.count()
    return_station_count = tashu_frame.groupby('RETURN_STATION').RETURN_STATION.count()
    
    sum_station_count = rent_station_count.add(return_station_count, fill_value=0).astype(int)
    sum_station_count.sort_values(inplace=True, ascending=False)
    top10_station_count = sum_station_count[:10]
    top10_station_number = top10_station_count.index

    result = []
    for i in range(0,10):
        result.append([
            station_name[top10_station_number[i]], 
            top10_station_number[i], 
            top10_station_count[i]
        ])

    return result

def get_top10_trace(tashu_dict, station_dict):
    """
    [역할]
    경로 Top10 출력하기
    (대여정류장, 반납정류장)의 빈도수 Top10

    [입력]
    tashu_dict : csv.DictReader 형태의 타슈대여정보
    station_dict : csv.DictReader 형태의 정류장 정보

    [출력]
    Top10 경로 리스트
    ex.) [[출발정류장 이름1, 출발정류장 번호1, 반납정류장 이름1,
        반납정류장 번호2, 경로 count], [출발정류장 이름2, 출발정류장 번호2,
        반납정류장 이름2,  반납정류장 번호2, 경로count2], .....] 형태
    """

    tashu_frame = pd.DataFrame(list(tashu_dict))
    station_frame = pd.DataFrame(list(station_dict))

    station_name = pd.Series(
        list(station_frame['NAME']), 
        index=list(station_frame['NUMBER'])
    )

    tashu_frame['TRACE'] = (tashu_frame['RENT_STATION'] 
                            + '-' 
                            + tashu_frame['RETURN_STATION'])

    trace_count = tashu_frame.groupby('TRACE').TRACE.count()
    trace_count.sort_values(inplace=True, ascending=False)

    top10_trace_count = trace_count[:10]
    top10_trace = top10_trace_count.index
    
    result = []
    for i in range(0, 10):
        trace = top10_trace[i]
        trace_split = trace.split('-')
        rent_station_number = trace_split[0]
        return_station_number = trace_split[1]
        result.append([
            station_name[rent_station_number], 
            rent_station_number, 
            station_name[return_station_number], 
            return_station_number, 
            top10_trace_count[i]
        ])

    return result

