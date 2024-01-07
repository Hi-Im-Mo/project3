# Historical Airline Delays & Cancellations Analysis
This project is the source code for an interactive analytical dashboard, found [here](http://airlinednc.us-east-1.elasticbeanstalk.com/), useful for uncovering historical flight status trends for domestic US flights based on the United States Depart of Transportation's [Bureau of Transportation](https://www.bts.gov/) data on flight statuses. 

#### -- Project Status: [Completed]

## Project Intro
The objective of this project is to visualize the data provided by the Bureau of Transportation in a meaningful way so as to glean insights on historical geographical trends as well as historical airline carrier and airport trends that affect the status of any given domestic flight in a user-friendly format. We largely utilized Plotly for any given rendering of the data and we used various algorithms to transform the data into more meaningful statistics for data analysis. Our team developed this dashboard in order to create a presentation on what airports are the best options to flight out of if you do not want to be delayed as well as the best carriers at those airports and a variety of other conclusions like geographical trends and historical averages that would be useful to the average flight consumer. 

### Methods Used
* Data Cleaning
* Database Design
* Interactive Data Visualization
* Frontend Web Application Development
* Website Containerization & Deployment

### Technologies
* Python
* AWS ElasticBeanstalk & Flask Server Deployment
* PostgreSQL Relational Database Design
* Pandas, NumPy, jupyter
* HTML & CSS
* Bootstrap Stylization Components
* Plotly.express Data Visualization
* Leaflet & Folium geoJSON Visualization

## Project Description
The project is webhosted using AWS ElasticBeanstalk environment using EC2 instances. The web application is developed on Flask using Python to code the visualizations, convert them into JSON data files to be interpretted by minimal JavaScript and then rendering and styled on HTML & CSS files. We created a home page to shower overarching trends in flight status data, which contains a line graph spanning from 2004 to 2023 showing the average percentage of delayed flights across all airports and carriers as well as a heatmap with an interactive HTML dropdown menu to select a year for the visualization of all airports and all carriers giving their respective number of delayed flights for the given year. The "Airports" and "Carriers" tabs on the navbar of the website lead to webpages containing visualizations based on airport or carrier respectively. For example, the "Airports" tab contains an interactive line graph of all the top 25 airports in the US giving their average percentage of delayed flights across carriers for the same year span as the home page graph, and the same thing is shown on the "Carriers" tab, but with respect to all of the carriers across our 2 decade span. Below this line graph on both tabs, we have an interactive HTML dropdown component to select a given airport or carrier and visualize a bar chart giving the average minutes a given flight is delayed for each carrier or airport derpending on the page. This is accompanied by a table showing the total amount of arriving flights for a given airport showing all carriers or a given carrier at all airports. Below these visualizations, we have another interactive HTML component that visualizes the "why" of flight delays. This component works the same on both tabs, but the specifications are different based on the webpage. For instance, if you are on the "Airports" tab, the user first selects the airport to visualize and then inputs textually the carrier to breakdown the reasons for delay at this given combination on an interactive pie chart. The last extension of the main webpage renders an interactive georgraphical rendering of the delay and cancellation hotspots across the US. This rendering is made possible through a plugin called folium and processes geoJSON using D3.js libraries. All in all, our web application provides a sufficient, user-friendly solution to answering any question on historical flight status statistics across of the US. 

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. To run the web application locally, execute the [app.py](app.py) file from your terminal.
3. Raw Data is being kept [here](data/rawYearlyData) within this repo.  
4. Data processing/transformation scripts are being kept [here](scripts)
5. Templates for rending the website are being kept [here](templates)
6. "[dataDescriptions](dataDescriptions.xlsx)" is an Excel spreadsheet containing descriptions of the data tags in our raw data.

## Contributing Members

|Name     |  Email   | 
|---------|-----------------|
|[Karson Kosek](https://github.com/kkosek-dev)| kkosek@alum.utk.edu |
|[Morgan Escue](https://github.com/Hi-Im-Mo) | morganabbigail2014@gmail.com |
|[Forest Prodan](https://github.com/forest-prodan) | forestprodan@gmail.com |
|[William Smalley](https://github.com/WSmalley) | williambsmalley1@gmail.com |

## Contact
* Feel free to contact team leads with any questions or if you are interested in contributing!
