library(ggplot2)
library(ggmap)

tashu = read.csv("tashu.csv")
rent_count = data.frame(table(tashu$RENT_STATION))
return_count = data.frame(table(tashu$RETURN_STATION))

sum_count <- merge(x = rent_count, y = return_count, 
                   by = c("Var1"), all = TRUE)
sum_count$Sum <- rowSums(sum_count[,c("Freq.x", "Freq.y")], 
                    na.rm = TRUE)
sum_count <- sum_count[order(-sum_count$Sum),]
top10_station <- sum_count[1:10,]

ggplot(data = top10_station, aes(x = Var1, y = Sum/1000, fill = Var1)) + 
  geom_bar(stat="identity") + 
  xlab("Station Number") + 
  ylab("Frequency (thousand)") + 
  ggtitle("Top 10 tashu station") + 
  theme(plot.title = element_text(hjust = 0.5))

station = read.csv("station.csv")
station_merge <- merge(station, sum_count, by.x = c("NUMBER"), by.y = c("Var1"))
daejon_gc <- geocode("Daejon")
daejon_cent <- as.numeric(daejon_gc)
ggmap(get_googlemap(center=daejon_cent, scale = 1,maptype = "roadmap",zoom=13)) + 
  geom_point(aes(x = LON, y = LAT, colour = "red", size = Sum), 
             data = station_merge, alpha = 0.5) +
  xlab("Lon") +
  ylab("Lat") +
  ggtitle("Tashu usage rate by station") + 
  theme(plot.title = element_text(hjust = 0.5))

trace_count <- data.frame(table(tashu$RENT_STATION, tashu$RETURN_STATION))
trace_count <- trace_count[order(-trace_count$Freq),]
top20_trace <- trace_count[1:20,]

qplot(Var1, Var2, data = top20_trace, size = Freq) + 
  xlab("Station Number") +
  ylab("Station Number") +
  ggtitle("Top 20 tashu trace") + 
  theme(plot.title = element_text(hjust = 0.5))
