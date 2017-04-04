# Import libraries
library(ggplot2)
library(scales)

# Read csv file
steps <- read.csv("steps.csv")

# Add all steps by each person
total_steps <- data.frame(colnames(steps[,-1]), 
                            colSums(steps[,-1]))
colnames(total_steps) <- c("name", "steps")


# Sort descending by sum steps
total_steps <- total_steps[order(-total_steps$steps),]

# Select top 10 steps
top10_steps <- total_steps[1:10,]

# Show top 10 steps bar graph
ggplot(data = top10_steps, aes(x = name, y = steps, fill = name)) + 
  geom_bar(stat = "identity") + 
  scale_y_continuous(labels = comma) + 
  ggtitle("Top 10 steps") + 
  theme(plot.title = element_text(hjust = 0.5))

