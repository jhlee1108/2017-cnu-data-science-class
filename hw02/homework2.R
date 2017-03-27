## Import libraries
library(ggplot2)
library(ggmap)

## Read csv files
tashu = read.csv("tashu.csv")
station = read.csv("station.csv")

## Count station usage
rent_count = data.frame(table(tashu$RENT_STATION))
return_count = data.frame(table(tashu$RETURN_STATION))

## Merge rent_count, return_count group by station number
sum_count <- merge(x = rent_count, y = return_count, by = c("Var1"), all = TRUE)

## Sum rent, return count
sum_count$Sum <- rowSums(sum_count[,c("Freq.x", "Freq.y")], na.rm = TRUE)

## Sort descending by sum count
sum_count <- sum_count[order(-sum_count$Sum),]

## Select top 10 station
top10_station <- sum_count[1:10,]

## Top 10 tashu station frequency bar graph
ggplot(data = top10_station, aes(x = Var1, y = Sum/1000, fill = Var1)) + 
  geom_bar(stat="identity") + 
  xlab("Station Number") + 
  ylab("Frequency (thousand)") + 
  ggtitle("Top 10 tashu station frequency") + 
  theme(plot.title = element_text(hjust = 0.5))

## Merge station, sum_count group by station number
station_merge <- merge(station, sum_count, by.x = c("NUMBER"), by.y = c("Var1"))

## lon : 127.3845, lat : 36.35041
daejon_gc <- geocode("Daejon")
daejon_cent <- as.numeric(daejon_gc)

## Tashu station frequency map
ggmap(get_googlemap(center = daejon_cent, scale = 1,maptype = "roadmap",zoom = 13)) + 
  geom_point(x = station_merge$LON, y = station_merge$LAT, colour = "red", 
             size = station_merge$Sum/30000, data = station_merge, alpha = 0.5) +
  xlab("Lon") +
  ylab("Lat") +
  ggtitle("Tashu station frequency map") + 
  theme(plot.title = element_text(hjust = 0.5))

## Count trace usage
trace_count <- data.frame(table(tashu$RENT_STATION, tashu$RETURN_STATION))

## Sort descending by trace count
trace_count <- trace_count[order(-trace_count$Freq),]

## Select top 20 trace
top20_trace <- trace_count[1:20,]

## Top 20 tashu trace graph
qplot(Var1, Var2, data = top20_trace, size = Freq) + 
  xlab("Rent station") +
  ylab("Return station") +
  ggtitle("Top 20 tashu trace") + 
  theme(plot.title = element_text(hjust = 0.5))
