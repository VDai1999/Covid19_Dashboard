#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#


## Fix Date: the upper bound needs to be larger than the lower bound

# Load the libraries
library(shiny)
library(tidyverse)
library(ggplot2)
library(lubridate)
library(plotly)
library(scales)
library(xtable)

# Call the data.R file created before
source('data.R')

# Assign each country with a distinct color
names(country_color) <- country$Country.Region

# Option to choose in the time series plot
stat_choices <- c('Number of Confirmed Cases' = 'ConfirmNum',
                  'Number of Death Cases' = 'DeathNum',
                  'Number of Recovered Cases' = 'RecoverNum')


# Assign each continent a color
names(cont_color) <- sort(cont_choices$Continent)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Coronavirus Statistics"),

    sidebarPanel(
        # The first tab: Time Series Plot
        conditionalPanel(condition = "input.tabs == 'Time Series Plot'",
                         selectInput(inputId="stat", label="Select a Category",
                                     choices=stat_choices),
                         
                         selectInput(inputId="country", label="Select Country",
                                     choices=virus$Country.Region, 
                                     multiple = TRUE,
                                     selected='World', 
                                     selectize = TRUE),
                         
                         dateRangeInput(inputId = "dates", label="Pick Date Range",
                                        start=min(virus$Date), end=max(virus$Date))
                         ),
        # The second tab: Bubble Plot
        conditionalPanel(condition = "input.tabs == 'Bubble Plot'",
                         selectInput(inputId="continent", label="Select a Continent",
                                     choices=cont_choices$Continent,
                                     multiple = TRUE,
                                     selected="Asia"),
                         sliderInput(inputId = 'date',label = "",
                                     min=min(virus$Date), max=max(virus$Date),
                                     value=min(virus$Date), dragRange = FALSE,
                                     animate = animationOptions(interval= 300))
        ),
      
    ),

        mainPanel(
            tabsetPanel(id='tabs',
                        tabPanel("Time Series Plot",  plotlyOutput(outputId = "timePlot")),
                        tabPanel("Bubble Plot", plotlyOutput(outputId = 'bubblePlot'))
            )
        )
    )



# Define server logic
server <- function(input, output, session) {
  
  # First plot: Time plot
  output$timePlot <- renderPlotly({
      # Select only the range that a user chose
      plot1 <- virus %>%
          filter(Date <= max(ymd(input$dates)),
                 Date >= min(ymd(input$dates)),
                 Country.Region %in% input$country)
      
      # Create a plot
      p1 <- ggplot(plot1) +
          geom_line(aes_string(x='Date', y=input$stat, color='Country.Region')) +
          geom_point(aes_string(x='Date', y=input$stat, color='Country.Region')) +
          scale_y_continuous(labels =comma) +
          scale_color_manual(name = '',
                             values = country_color[input$country]) +
          theme_bw() +
          theme(plot.caption = element_text(size=12),
                axis.text = element_text(size = 12))
      
      # Create a plotly plot
      ggplotly(p1) %>%
        layout(title = paste0('The Time Series Plot of the ', names(stat_choices)[stat_choices==input$stat]),
               xaxis=list(
               title = 'Date
                <br>                                                     Source: JHU CSSE',
                titlefont = list(size = 14),
                tickfont = list(size = 10)),
                margin = list(l = 50, r = 50, t = 60, b = 60),
                yaxis = list(title = names(stat_choices)[stat_choices==input$stat],
                            titlefont = list(size = 14),
                            tickfont = list(size = 10)))
      
  }) 
  
  # The second plot: Bubble plot
  output$bubblePlot <- renderPlotly({
      # Select only continent that a use picked
      plot2 <- virus %>%
          filter(Continent %in% input$continent)
      
      # Specify the maximum of the x- and y-axis
      max_xaxis <- max(plot2$DeathNum)
      max_yaxis <- max(plot2$RecoverNum)
      
      # Select the beginning date that a use chose
      plot2 <- plot2 %>%
        filter(Date == input$date)
      
      # Create a plot
      p2 <- ggplot(plot2, aes(label = Country.Region)) +
        geom_point(aes_string(x='DeathNum', y='RecoverNum', 
                              size='ConfirmNum', color='Continent'),
                   alpha = 0.5) +
        scale_color_manual(name = '',
                           values = cont_color[input$continent]) +
        scale_x_continuous(limits = c(0, max_xaxis),
                           labels = comma) +
        scale_y_continuous(limits = c(0, max_yaxis),
                           labels = comma) +
        theme_bw()
      
      # Create a plotly plot
      ggplotly(p2) %>%
        layout(title = paste0('The relationship between the number of Death Cases and the Recovered Cases by Continent'),
               titlefont=list(size =16),
               xaxis=list(
                 title = '<br><br><br><br>Number of Death Cases
                 <br>                                                     Source: JHU CSSE
                 
                           * Each bubble represents for a country
                           ** The bubble\'s size represents for the number of confirmed Cases',
                 titlefont = list(size = 14),
                 tickfont = list(size = 10)),
               yaxis = list(title = "Number of Recovered Cases",
                            titlefont = list(size = 14),
                            tickfont = list(size = 10)))
      
  })
    
}

# Run the application 
shinyApp(ui = ui, server = server)
