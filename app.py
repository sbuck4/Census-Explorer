import streamlit as st
from config import ALL_STATES, STATE_CODES
from data_retrieval import get_city_and_state_data, get_city_employment_by_industry_data
from utils import prepare_dataframe_for_display, download_options
from walmart import has_walmart
import warnings
import urllib3

# Suppress specific urllib3 warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)

def main():
    st.set_page_config(page_title="Census Data Explorer", layout="wide")
    
    st.title("Census Data Explorer")
    st.markdown("Access demographic data from the ACS and view additional data columns.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        state_input = st.selectbox("Select a State:", ALL_STATES)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Search", use_container_width=True)
    
    if search_button:
        state_code_value = STATE_CODES.get(state_input)
        if state_code_value:
            st.write(f"Fetching ACS data for {state_input} (State Code: {state_code_value})...")
            acs_df = get_city_and_state_data(state_code_value)
            if acs_df is not None and not acs_df.empty:
                st.subheader(f"ACS Data for Cities in {state_input}")
                display_df = prepare_dataframe_for_display(acs_df)
                
                # Merge dominant industry data by city using the condensed labels
                dominant_df = get_city_employment_by_industry_data(state_code_value)
                if dominant_df is not None and not dominant_df.empty:
                    display_df = display_df.merge(dominant_df[['City', 'Dominant Industry']], on='City', how='left')
                    # Overwrite the original Industry column with the condensed value
                    display_df["Industry"] = display_df["Dominant Industry"]
                else:
                    display_df["Industry"] = "Industry not reported"
                
                # Add Walmart column
                display_df["Walmart in Town?"] = display_df["City"].apply(has_walmart)
                
                # Create new column combining City and Population
                display_df["PLACE ~ POPULATION"] = display_df.apply(
                    lambda row: f"{row['City']} ~ {row['Population']}", axis=1
                )
                
                # Final display order
                display_columns = [
                    "PLACE ~ POPULATION",
                    "Median Income",
                    "Poverty Rate (%)",
                    "Industry",
                    "Over 55 (%)",
                    "White (%)",
                    "Black (%)",
                    "Walmart in Town?"
                ]
                
                st.dataframe(display_df[display_columns], use_container_width=True)
                
                st.subheader("Download Data")
                download_files = download_options(display_df[display_columns], state_input)
                st.download_button(
                    label="Download as CSV",
                    data=download_files['csv']['data'],
                    file_name=download_files['csv']['filename'],
                    mime=download_files['csv']['mime']
                )
                if 'excel' in download_files:
                    st.download_button(
                        label="Download as Excel",
                        data=download_files['excel']['data'],
                        file_name=download_files['excel']['filename'],
                        mime=download_files['excel']['mime']
                    )
            else:
                st.warning("No ACS data available for the selected state.")
        else:
            st.error("State name not recognized.")

if __name__ == "__main__":
    main()
