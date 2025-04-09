# Census Data Explorer

Census Data Explorer is a Streamlit application that allows users to explore city-level demographic data from the American Community Survey (ACS). The application displays formatted ACS data alongside additional information such as the dominant employment industry (with condensed labels) and whether a Walmart store is within a specified distance of a given city. Data can be downloaded as CSV or Excel files for further analysis.

## Features

- **ACS Data Retrieval:**  
  Fetches demographic data from the U.S. Census Bureau’s ACS API for the selected state. Data includes population, median household income, poverty rates, racial percentages, age distributions, and industry employment data.

- **Dominant Industry Determination:**  
  The application calculates the dominant employment industry for each city using data provided by the ACS. The industry data is condensed into one of the following labels based on a custom mapping:  
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
  Determines whether a Walmart store is located within a 10-mile radius of the city using geocoding (with the [Nominatim](https://nominatim.openstreetmap.org/) service) and a CSV file of Walmart locations sourced from Kaggle.

- **Data Presentation and Export:**  
  Displays a table in the following order:  
  - **PLACE ~ POPULATION** (City and Population combined)  
  - **Median Income**  
  - **Poverty Rate (%)**  
  - **Industry** (Dominant industry using condensed labels)  
  - **Over 55 (%)**  
  - **White (%)**  
  - **Black (%)**  
  - **Walmart in Town?**  
  Users can download the displayed data in CSV or Excel formats.

## Data Sources

- **American Community Survey (ACS):**  
  The application pulls data from the Census Bureau’s ACS API ([API Documentation](https://www.census.gov/data/developers/data-sets/acs-1year.html)). The ACS provides detailed demographic, social, economic, and housing data for the United States. The data used in this application is drawn from the 2023 ACS 1-Year Supplemental Estimates. Information such as total population, median household income, poverty rates, and industry employment are sourced directly through this API.

- **Walmart Store Locations:**  
  A CSV file containing Walmart store locations across the United States is used to determine proximity to a city. This CSV file was originally sourced from Kaggle (e.g., via the dataset "Walmart Store Locations Across the United States"). The application reads this file locally to perform distance calculations.

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd Demographic
