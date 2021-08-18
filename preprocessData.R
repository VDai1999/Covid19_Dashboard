# Load libraries
library(tidyverse)
library(lubridate)
library(maps)
library(ggmap)


# Read the data
us <- read.csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv",
               sep=",",
               header=TRUE)
states <- read.csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
                   sep=",",
                   header=TRUE)

# CLEAN THE DATASETS
# US dataset
# Change the date column from character format to date format
us$date <- ymd(us$date)
# Calculate the daily cases and daily deaths
us$daily_cases <- c(us[1,2], diff(us$cases))
us$daily_deaths <- c(us[1,3], diff(us$deaths))


# States dataset
# Change the date column from character format to date format and state column from character to factor format
states <- states %>%
  mutate(date = ymd(date),
         state = factor(state))
# Check to see if we calculate the right daily cases and daily deaths
states <- states %>%
  group_by(state) %>%
  mutate(N = row_number(),
         daily_cases = ifelse(N == 1, cases, cases - lag(cases)),
         daily_deaths = ifelse(N == 1, deaths, deaths - lag(deaths))) %>%
  select(-N)


# Read the region dataset
regions <- read.csv("https://raw.githubusercontent.com/cphalpert/census-regions/master/us%20census%20bureau%20regions%20and%20divisions.csv",
                    sep=",",
                    header=TRUE)

# Puerto Rico, Virgin Islands, Guam, Northern Mariana Islands are not assigned to a specific region; therefore, we will keep
# their original labels
regions <- rbind(regions,
                 data.frame(State=c("Puerto Rico","Virgin Islands", "Guam", "Northern Mariana Islands"),
                            State.Code=c("RR", "VI", "GU", "MP"),
                            Region=c("Other","Other", "Other", "Other"),
                            Division=c("None", "None", "None", "None")))

# Merge the Region column to states dataframe
states <- merge(states, regions[, c("State", "Region")], by.x=c("state"), by.y=c("State"), all.x = TRUE) # Merge
states$Region <- factor(states$Region,
                        levels=c("Northeast", "Midwest", "West", "South", "Other")) # Transform data type

# Rename variables
states <- states %>%
  rename(State = state,
         Date = date,
         Total_Cases = cases,
         Total_Deaths = deaths,
         Daily_Cases = daily_cases,
         Daily_Deaths = daily_deaths)


# Load the state data set provided in the map library
state <- map_data("state")
# Change the case (first letter) of the region column
state$region <- str_to_title(state$region)

