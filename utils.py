import pandas as pd
import io

def map_industry_code(var_code):
    mapping = {
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
    return mapping.get(str(var_code).strip(), "Industry not reported")

def prepare_dataframe_for_display(result_df):
    display_df = result_df.copy()
    if 'Population' in display_df.columns:
        display_df['Population'] = display_df['Population'].fillna(0).astype(int).apply(lambda x: f"{x:,}")
    if 'Median Income' in display_df.columns:
        display_df['Median Income'] = display_df['Median Income'].fillna(0).astype(int).apply(lambda x: f"${x:,}")
    for col in ['Poverty Rate (%)', 'White (%)', 'Black (%)', 'Over 55 (%)']:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "N/A")
    return display_df

def download_options(result_df, state_name):
    downloads = {}
    csv_buffer = io.StringIO()
    result_df.to_csv(csv_buffer, index=False)
    downloads['csv'] = {
        'data': csv_buffer.getvalue(),
        'filename': f"{state_name}_census_data.csv",
        'mime': "text/csv"
    }
    try:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            result_df.to_excel(writer, sheet_name='Census Data', index=False)
        downloads['excel'] = {
            'data': excel_buffer.getvalue(),
            'filename': f"{state_name}_census_data.xlsx",
            'mime': "application/vnd.ms-excel"
        }
    except ImportError:
        pass
    return downloads
