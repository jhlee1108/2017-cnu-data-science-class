library(ggplot2)

sleep <- read.csv('sleep.csv')

ggplot(data = sleep, aes(x=start, y=end)) + 
  geom_point(aes(colour=name)) + 
  xlab("time to bed") + 
  ylab("time to wake up")
