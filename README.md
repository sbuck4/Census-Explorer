# Census Data Explorer

Access demographic data from the U.S. Census Bureau's American Community Survey, merged with additional data columns (e.g., dominant employment industry using condensed labels and Walmart proximity). This interactive Streamlit application enables easy exploration of census data and exports for further analysis.

![Screenshot of the City Demographic Application](https://raw.githubusercontent.com/sbuck4/Census-Explorer/main/images/streamlitSC.jpeg)

## Features

- **ACS Data Retrieval:**  
  Fetches city-level demographic data from the U.S. Census Bureau’s ACS API for the selected state. Data includes population, median household income, poverty rates, racial percentages, age distributions, and industry employment data.

- **Dominant Industry Determination:**  
  Uses ACS employment data to determine the dominant industry for each city. Industries are condensed into one of the following labels:
  - Ag/Fish/Mining
  - Construction
  - Manufacturing
  - Wholesale
  - Retail
  - Transport/Utilities
  - Information
  - Finance/Real Estate
  - Professional/Administrative
  - Education/Health
  - Arts/Food Services
  - Other Services
  - Public Admin

- **Walmart Proximity Check:**  
  Determines whether a Walmart store is located within a 10-mile radius of each city by geocoding the city name and calculating the distance from the city to each Walmart location (data sourced from a CSV file).

- **Data Presentation and Export:**  
  Displays data in the following order:
  - **PLACE ~ POPULATION** (City name combined with population)
  - **Median Income**
  - **Poverty Rate (%)**
  - **Industry** (Dominant industry using condensed labels)
  - **Over 55 (%)**
  - **White (%)**
  - **Black (%)**
  - **Walmart in Town?**  
  Users can download the displayed data as CSV or Excel files.

## Data Sources

- **American Community Survey (ACS):**  
  Data is fetched from the U.S. Census Bureau’s ACS API ([API Documentation](https://www.census.gov/data/developers/data-sets/acs-1year.html)). This app uses data from the 2023 ACS 1-Year Supplemental Estimates, which provides detailed demographic, economic, and employment information.

- **Walmart Store Locations:**  
  A CSV file containing Walmart store locations across the United States is used to determine Walmart proximity. This data was sourced from a dataset on Kaggle and is stored locally.

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/sbuck4/Census-Explorer.git
   cd Demographic
