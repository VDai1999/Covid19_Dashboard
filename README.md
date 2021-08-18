![Logo](https://cdnuploads.aa.com.tr/uploads/Contents/2020/03/31/thumbs_b_c_f0c9e70408e03dcbd2c231d82228c08b.jpg?v=210121)

# Covid19 R-Shiny Dashboard

### Description
This dashboard allows users to view the overall summary statistics of COVID-19 in the U.S. This app also let users to interact with the app to see trend by region and by state.

## Installation

This project requires **R version 4.0.3** with **R Studio Version 1.3.1093** installed. Also, it requires having an account on [shinyapps.io](https://www.shinyapps.io/).

### R
[Install R](https://www.r-project.org/)

### R Studio
[Install R Studio](https://www.rstudio.com/products/rstudio/download/)


## Appendix

Libraries used:
```{r}
library(shiny)
library(shinythemes)
library(tidyverse)
library(shinydashboard)
library(lubridate)
library(plotly)
library(scales)
library(stringr)
library(ggthemes)
library(maps)
library(ggmap)
```

## Acknowledgements
The retrieved data is [Coronavirus (Covid-19) Data in the United States](https://github.com/nytimes/covid-19-data)
