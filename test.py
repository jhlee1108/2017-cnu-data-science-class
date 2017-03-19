import csv

tashu_file = open('station.csv', 'r')
tashu = csv.DictReader(tashu_file)

for rent in tashu:
    coordinates = rent['COORDINATES']
    lat, lon = coordinates.split(',')
    print(str(lon) + ',' + str(float(lat)))
