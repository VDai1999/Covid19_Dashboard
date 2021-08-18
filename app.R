# load libraries
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


# Set a working directory: only needed when running locally
#setwd("~/")


# Call the preprocessData.R file
source('preprocessData.R')

ui <- dashboardPage(
  dashboardHeader(title = "COVID-19 Dashboard"), # dashboardHeader
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Summary Statistics", 
               tabName = "tab1"),
      menuItem("Regional Trend", tabName = 'tab2'),
      menuItem("Map", tabName = 'tab3')
    ) # sidebarMenu
    
  ), # dashboardSidebar
  
  dashboardBody(
    tabItems(
      tabItem(tabName = "tab1",
              
              fluidRow(
                # Ask user to select a date range
                dateInput(inputId = 'date_t1', label = 'Select a date', 
                          min = min(us$date), max = max(us$date),
                          value = max(us$date))
                ), # fluidRow
              
              # First row display cumulative counts
              fluidRow(
                # Display the number of daily cases and daily deaths by a
                # selected date range
                infoBoxOutput("Total_Cases"),
                infoBoxOutput("Total_Deaths")
              ), # fluidRow
              
              fluidRow(
                # Display the number of total cases and total deaths by a
                # selected date range
                infoBoxOutput("Daily_Cases"),
                infoBoxOutput("Daily_Deaths")
              ), # fluidRow
              
              hr(),
              
              fluidRow(
                # Select the top # to view the top # of states in 4 different categories
                radioButtons("top", "Select a number to view the top # states", choices = c('5', '10', '15'))
                ),
              
              fluidRow(
                # Output of the the top # states in total cases and total deaths
                box(tableOutput('table1')),
                box(tableOutput('table2'))
              ),
              
              fluidRow(
                # Output of the the top # states in daily cases and daily deaths
                box(tableOutput('table3')),
                box(tableOutput('table4'))
              )
              
              ), # tabItem: tab1
      
      tabItem(tabName = "tab2",
              # Regional Trend tab
              
              # Filter
              fluidRow(
                # Ask a user to select a date range
                box(dateRangeInput(inputId = 'dateRange1', label = 'Pick a range of date',
                                   start = min(us$date), end = max(us$date))),
                # Ask a user to select a category
                box(selectInput(inputId="stat", label="Select a category",
                                choices = c("Daily Cases" = "Daily_Cases", "Daily Deaths" = "Daily_Deaths", 
                                            "Total Cases" = "Total_Cases", "Total Deaths" = "Total_Deaths"), 
                                multiple = FALSE,
                                selected = 'Daily Cases', 
                                selectize = TRUE))
              ), # fluidRow
              
              # Output of a plot
              plotlyOutput("bbPlot")
        
      ), # tabItem: tab2
      
      tabItem(tabName = "tab3",
              # Map tab
              
              # Filter
              fluidRow(
                # Ask a user to select a date range
                box(dateInput(inputId = 'date_t3', label = 'Select a date', 
                          min = min(us$date), max = max(us$date),
                          value = max(us$date))),
                
                # Ask a user to select a category
                box(selectInput(inputId="stat_t3", label="Select a category",
                                choices = c("Daily Cases" = "Daily_Cases", "Daily Deaths" = "Daily_Deaths", 
                                            "Total Cases" = "Total_Cases", "Total Deaths" = "Total_Deaths"), 
                                multiple = FALSE,
                                selected = 'Daily Cases', 
                                selectize = TRUE))
              ), # fluidRow
              
              # Output of a map
              plotlyOutput("map1")
              ) # tabItem: tab 3
      
    ) # tabItema
    
  ) # dashboardBody
) # ui

server <- function(input, output) {
  
  # create a data set that matched the selected input of a user in tab 1
  dat <- reactive( {us %>% filter(date == input$date_t1)} )
  dat_state <- reactive( {states %>% 
      filter(Date == input$date_t1) 
    } )
  
  output$Total_Cases <- renderInfoBox({
    # Generate an output box that displays the total COVID-19 cases in the U.S
    
    infoBox(title = "Total Cases",
            value = dat()$cases,
            icon = icon("fas fa-viruses"),
            fill = TRUE)
  })
  
  output$Total_Deaths <- renderInfoBox({
    # Generate an output box that displays the total COVID-19 deaths in the U.S
    
    infoBox(title = "Total Deaths",
            value = dat()$deaths,
            icon = icon("fas fa-skull-crossbones"),
            fill = TRUE)
  })
  
  output$Daily_Cases <- renderInfoBox({
    # Generate an output box that displays the daily COVID-19 cases in the U.S
    
    infoBox(title = "Daily Cases",
            value = dat()$daily_cases,
            icon = icon("fas fa-viruses"),
            fill = TRUE)
  })
  
  output$Daily_Deaths <- renderInfoBox({
    # Generate an output box that displays the daily COVID-19 deaths in the U.S
    
    infoBox(title = "Daily Deaths",
            value = dat()$daily_deaths,
            icon = icon("fas fa-skull-crossbones"),
            fill = TRUE)
  })
  
  output$table1 <- renderTable({
    # Generate an output table that displays the top # states that have the 
    # highest total cases
    
    dat_state() %>%
      select(c(State, Total_Cases)) %>%
      arrange(desc(Total_Cases)) %>%
      mutate('#' = row_number()) %>%
      select(c('#', State, Total_Cases)) %>%
      rename('Total Cases' = Total_Cases) %>%
      group_by(State) %>%
      head(input$top)
  })
  
  output$table2 <- renderTable({
    # Generate an output table that displays the top # states that have the 
    # highest total deaths
    
    dat_state() %>%
      select(c(State, Total_Deaths)) %>%
      arrange(desc(Total_Deaths)) %>%
      mutate('#' = row_number()) %>%
      select(c('#', State, Total_Deaths)) %>%
      rename('Total Deaths' = Total_Deaths) %>%
      group_by(State) %>%
      head(input$top)
  })
  
  output$table3 <- renderTable({
    # Generate an output table that displays the top # states that have the 
    # highest daily cases
    
    dat_state() %>%
      select(c(State, Daily_Cases)) %>%
      arrange(desc(Daily_Cases)) %>%
      mutate('#' = row_number()) %>%
      select(c('#', State, Daily_Cases)) %>%
      rename('Daily Cases' = Daily_Cases) %>%
      group_by(State) %>%
      head(input$top)
  })
  
  output$table4 <- renderTable({
    # Generate an output table that displays the top # states that have the 
    # highest daily deaths
    
    dat_state() %>%
      select(c(State, Daily_Deaths)) %>%
      arrange(desc(Daily_Deaths)) %>%
      mutate('#' = row_number()) %>%
      select(c('#', State, Daily_Deaths)) %>%
      rename('Daily Deaths' = Daily_Deaths) %>%
      group_by(State) %>%
      head(input$top)
  })
  
  output$bbPlot <-  renderPlotly({
    # Regional trend plot
      
    # Create a dataframe that matches the selected date range
    bbPlot_df <- states %>%
      filter(Date <= max(ymd(input$dateRange1)),
             Date >= min(ymd(input$dateRange1)))
    
    # Calculate the summation of the selected statistic by date and by region
    bbPlot_df <- aggregate(bbPlot_df[input$stat], by=list(Date=bbPlot_df$Date, Region=bbPlot_df$Region), FUN=sum)
    
    # Plot
    bbPlot <- ggplot(bbPlot_df) +
      geom_line(aes_string(x='Date', y=input$stat, color='Region'),
                 alpha = 0.5, size=0.5) +
      geom_point(aes_string(x='Date', y=input$stat, color='Region'),
                alpha = 0.5, size=1) +
      scale_y_continuous(labels = comma) +
      theme_bw() +
      theme(legend.title = element_blank())
    
    
    ggplotly(bbPlot)
  })
  
  output$map1 <- renderPlotly({
    # Map
    
    # Create a dataframe that matches the selected date
    current_state_data <- states %>%
      filter(Date == input$date_t3)
    
    # Join the state dataframe (a given dataframe in the map library) and
    # the current_state_data
    us_map <- left_join(state, current_state_data, by=c("region"="State"))
    # Rename the region column
    us_map <- us_map %>%
      rename(State = region)
    
    # Create a map
    map_plot <- ggplot()+
      geom_polygon(aes_string(x="long", y="lat", group="group", fill=input$stat_t3, label="State"),
                   data=us_map) +
      scale_fill_continuous(labels = comma,
                            high = "#132B43", low = "#56B1F7") +
      theme_map()
    
    ggplotly(map_plot)
    })
  
}

shinyApp(ui, server)