import requests
import pandas as pd
from config import BASE_URL, API_KEY

def safe_numeric_convert(series, default=0):
    return pd.to_numeric(series, errors='coerce').fillna(default)

def get_city_and_state_data(state_code):
    variables = [
        "NAME",
        "K200101_001E",  # Total Population
        "K201902_001E",  # Median Household Income
        "K201801_001E",  # Total Poverty Count
        "K201801_002E",  # Below poverty level
        "K200201_002E",  # White alone
        "K200201_003E",  # Black or African American alone
        "K200104_007E",  # 55 to 64 years
        "K200104_008E",  # 65 years and over
        "K201703_001E"   # Industry data (basic)
    ]
    
    variables_str = ",".join(variables)
    url = f"{BASE_URL}?get={variables_str}&for=place:*&in=state:{state_code}&key={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        
        df['Clean_Name'] = df['NAME'].apply(
            lambda x: x.split(',')[0].replace(' city', '').replace(' town', '').replace(' CDP', '').replace(' (balance)', '')
        )
        df['Total_Population'] = safe_numeric_convert(df['K200101_001E'])
        df['Median_Household_Income'] = safe_numeric_convert(df['K201902_001E'])
        # Median Age removed
        df['Total_Poverty_Count'] = safe_numeric_convert(df['K201801_001E'])
        df['Below_Poverty_Count'] = safe_numeric_convert(df['K201801_002E'])
        df['White_Count'] = safe_numeric_convert(df['K200201_002E'])
        df['Black_Count'] = safe_numeric_convert(df['K200201_003E'])
        df['55_to_64'] = safe_numeric_convert(df['K200104_007E'])
        df['65_and-over'] = safe_numeric_convert(df['K200104_008E'])
        
        df['Poverty_Rate'] = (df['Below_Poverty_Count'] / df['Total_Poverty_Count'] * 100).round(2).fillna(0)
        df['White_Percentage'] = (df['White_Count'] / df['Total_Population'] * 100).round(2).fillna(0)
        df['Black_Percentage'] = (df['Black_Count'] / df['Total_Population'] * 100).round(2).fillna(0)
        df['Over_55_Population'] = df['55_to_64'] + df['65_and-over']
        df['Over_55_Percentage'] = (df['Over_55_Population'] / df['Total_Population'] * 100).round(2).fillna(0)
        
        df['Industry_Code'] = df['K201703_001E']
        df['Industry_Description'] = df['Industry_Code'].apply(lambda x: str(x).strip())
        
        result_df = df[['Clean_Name', 'Total_Population', 'Median_Household_Income', 'Poverty_Rate',
                        'White_Percentage', 'Black_Percentage', 'Over_55_Percentage', 
                        'Industry_Code', 'Industry_Description', 'state', 'place']]
        result_df = result_df.rename(columns={
            'Clean_Name': 'City',
            'Total_Population': 'Population',
            'Median_Household_Income': 'Median Income',
            'Poverty_Rate': 'Poverty Rate (%)',
            'White_Percentage': 'White (%)',
            'Black_Percentage': 'Black (%)',
            'Over_55_Percentage': 'Over 55 (%)',
            'Industry_Code': 'Industry Code',
            'Industry_Description': 'Industry',
            'state': 'State Code',
            'place': 'Place Code'
        })
        
        print("Result DataFrame columns:", result_df.columns.tolist())
        return result_df
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def get_city_employment_by_industry_data(state_code):
    base_vars = [
        "NAME",
        "K200101_001E",
        "K201902_001E",
    ]
    industry_vars = [
        "K202403_002E",  # Ag/Fish/Mining
        "K202403_003E",  # Construction
        "K202403_004E",  # Manufacturing
        "K202403_005E",  # Wholesale
        "K202403_006E",  # Retail
        "K202403_007E",  # Transport/Utilities
        "K202403_008E",  # Information
        "K202403_009E",  # Finance/Real Estate
        "K202403_010E",  # Professional/Administrative
        "K202403_011E",  # Education/Health
        "K202403_012E",  # Arts/Food Services
        "K202403_013E",  # Other Services
        "K202403_014E",  # Public Admin
    ]
    variables = base_vars + industry_vars
    variables_str = ",".join(variables)
    url = f"{BASE_URL}?get={variables_str}&for=place:*&in=state:{state_code}&key={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        
        df['Clean_Name'] = df['NAME'].apply(
            lambda x: x.split(',')[0].replace(' city', '').replace(' town', '').replace(' CDP', '').replace(' (balance)', '')
        )
        df['Total_Population'] = safe_numeric_convert(df['K200101_001E'])
        df['Median_Household_Income'] = safe_numeric_convert(df['K201902_001E'])
        
        for var in industry_vars:
            df[var] = safe_numeric_convert(df[var])
        
        # Use condensed industry labels as specified
        industry_labels = {
            "K202403_002E": "Ag/Fish/Mining",
            "K202403_003E": "Construction",
            "K202403_004E": "Manufacturing",
            "K202403_005E": "Wholesale",
            "K202403_006E": "Retail",
            "K202403_007E": "Transport/Utilities",
            "K202403_008E": "Information",
            "K202403_009E": "Finance/Real Estate",
            "K202403_010E": "Professional/Administrative",
            "K202403_011E": "Education/Health",
            "K202403_012E": "Arts/Food Services",
            "K202403_013E": "Other Services",
            "K202403_014E": "Public Admin"
        }
        
        def dominant_industry(row):
            max_val = 0
            dominant = "Industry not reported"
            for var in industry_vars:
                if row[var] > max_val:
                    max_val = row[var]
                    dominant = industry_labels.get(var, "Unknown")
            return dominant
        
        df["Dominant Industry"] = df.apply(dominant_industry, axis=1)
        
        result_df = df[['Clean_Name', 'K200101_001E', 'K201902_001E', 'Dominant Industry', 'state', 'place']]
        result_df = result_df.rename(columns={
            'Clean_Name': 'City',
            'K200101_001E': 'Population',
            'K201902_001E': 'Median Income',
            'state': 'State Code',
            'place': 'Place Code'
        })
        return result_df
    except requests.RequestException as e:
        print(f"Error fetching industry data: {e}")
        return None
