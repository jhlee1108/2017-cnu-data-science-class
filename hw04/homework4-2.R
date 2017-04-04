# Import library
library(ggplot2)

# Read csv file
sleep <- read.csv('sleep.csv')

# Show Time to bed and wake up
ggplot(data = sleep, aes(x=start, y=end)) + 
  geom_point(aes(colour=name)) + 
  xlab("time to bed") + 
  ylab("time to wake up") +
  ggtitle("Time to bed and wake up") +
  theme(plot.title = element_text(hjust = 0.5))
