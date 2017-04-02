# Import libraries
library(ggplot2)
library(scales)

# Read csv file
steps <- read.csv("steps.csv")

# Add all steps by each person
steps$sum <- rowSums(steps[,2:length(steps[1,])])

# Sort descending by sum steps
steps <- steps[order(-steps$sum),]

# Select top 10 steps
top10_steps <- steps[1:10,]

# Show top 10 steps bar graph
ggplot(data = top10_steps, aes(x = name, y = sum, fill = name)) + 
  geom_bar(stat = "identity") + 
  scale_y_continuous(labels = comma) + 
  ylab("steps") + 
  ggtitle("Top 10 steps") + 
  theme(plot.title = element_text(hjust = 0.5))

