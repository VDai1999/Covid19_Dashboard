# Load libraries
library(tidyverse)
library(lubridate)

# Create a function that change the wide to tall format, change the format 
# of the Date variable, and calculate the culmulative cases
dfTransform <- function(df) {
  df <- df%>%
    select(-Province.State, -Lat, -Long) %>%
    pivot_longer(cols = -Country.Region,
                 names_to = "Date", 
                 values_to = "numberofPeople") %>%
    mutate(Date = paste0("0", substring(Date, 2, nchar(Date))),
           Date = mdy(Date)) %>%
    group_by(Country.Region, Date) %>%
    summarise(TotalCases = sum(numberofPeople, na.rm=TRUE))
  
  return(df)
}

####################################
# Confirm Dataset
####################################
# Read in the data set that retrieved from John Hopskins University
global_confirmed <- read.csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", 
                             sep=",", 
                             header=TRUE)
# Transform the data frame
global_confirmed <- dfTransform(global_confirmed)
# Rename the TotalCases variable to ConfirmNum variable
global_confirmed <- global_confirmed %>%
  rename(ConfirmNum = TotalCases)

####################################
# Death Dataset
####################################
# Read in the data set that retrieved from John Hopskins University
global_deaths <- read.csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
                          sep=",",
                          header=TRUE)
# Transform the data frame
global_deaths <- dfTransform(global_deaths)
# Rename the TotalCases variable to DeathNum variable
global_deaths <- global_deaths %>%
  rename(DeathNum = TotalCases)

####################################
# Recover Dataset
####################################
# Read in the data set that retrieved from John Hopskins University
global_recovers <- read.csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
                            sep=',',
                            header=TRUE)
# Transform the data frame
global_recovers <- dfTransform(global_recovers)
# Rename the TotalCases variable to RecoverNum variable
global_recovers <- global_recovers %>%
  rename(RecoverNum = TotalCases)


# Merge 3 dataframes together
virus <- merge(global_confirmed, global_deaths, by=c("Country.Region", "Date"))
virus <- merge(virus, global_recovers, by=c("Country.Region", "Date"))


# Calculate the statistics for the whole world
world <- virus %>%
  mutate(Country.Region = "World",
         Date = Date) %>%
  group_by(Country.Region, Date) %>%
  summarise(ConfirmNum = sum(ConfirmNum, na.rm = TRUE),
            DeathNum = sum(DeathNum, na.rm = TRUE),
            RecoverNum = sum(RecoverNum, na.rm = TRUE)) %>%
  as.data.frame(world)

# Merge 2 dataframes together
virus <- rbind(virus, world)
virus <- virus %>%
  mutate(Country.Region = as.character(Country.Region))


# Read the continent data set
continent <- read.csv('https://raw.githubusercontent.com/dbouquin/IS_608/master/NanosatDB_munging/Countries-Continents.csv')
continent <- continent %>%
  mutate(Country = as.character(Country),
         Continent = as.character(Continent))

# Join 2 datasets together
virus <- left_join(virus, continent, by=c("Country.Region" =  "Country"))

# Find out which country is not assigned to a continent
df <- virus[is.na(virus$Continent),] %>%
  group_by(Country.Region) %>%
  summarise(N = n())

# Create a new dataframe which consists of countries/lands that
# are not included in the continent dataset 
ct <- c('Africa', 'Asia', 'Africa', 'Africa', 'Africa', 'Africa', 'Europe', 'Ship',
        'Africa', 'Europe', 'Europe', 'Ship', 'Europe', 'Asia/Europe', 'Asia',
        'Asia', 'Asia', 'Africa', 'NA')
temp <- data.frame("Country" = as.vector(df['Country.Region']), 'Continent' = ct)
temp$Continent <- as.character(temp$Continent)

virus$Continent[is.na(virus$Continent)] <- 'NA'


# Join the virus dataframe with the new dataframe just created
virus <- left_join(virus, temp, by=c("Country.Region" =  "Country.Region"))

# Transform the virus dataframe
virus <- virus %>%
  mutate(Continent.x = ifelse(Continent.x == 'NA', Continent.y, Continent.x)) %>%
  select(-Continent.y) %>%
  rename(Continent = Continent.x)


# List of country
country <- virus %>%
  group_by(Country.Region) %>%
  summarise(N = n())

# Read in the color dataset
colors_df <- read.csv('https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv', header = FALSE)

# Assign each country with each color
colors <- colors_df[c(1:nrow(country)),]
country_color <- as.character(colors$V3)

# List of categories used plot 2
cont_choices <- virus %>%
  filter(Continent %in% c('Asia', 'Africa', 'North America', 'South America', 
                          'Europe', 'Oceania', 'Asia/Europe')) %>%
  group_by(Continent) %>%
  summarize(N = n())

# Assigned each continent with a different color
cont_color <- rainbow(7)

