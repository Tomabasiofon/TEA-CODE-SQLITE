import os
import streamlit as st
from input.capex_input import get_capex_data
from input.opex_input import get_opex_data
from input.electrolyser_input import get_electrolyser_data
from input.pretreat import get_pretreat_equipment_cost_data
from input.cash_flow_input import get_cash_flow_data
from input.data_reader import populate_db_from_excel
from electrolyser_calc import electrolyser_formulae
from capex_calc import capex_formulae
from opex_calc import opex_formulae
from cash_flow_calc import cash_flow_formulae
from discounted_cash_flow import discounted_cash_flow_analysis

# Define paths
excel_file_path = 'data/input.xlsx'
db_file_path = 'data/database.db'

def get_file_last_modified_time(filepath):
    """Get the last modified time of the file to track changes."""
    return os.path.getmtime(filepath)

# @st.cache_data
def populate_database(last_modified):
    """Populate the database from the Excel file."""
    populate_db_from_excel(excel_file_path, db_file_path)

def main():
    """
    Main function to populate the database and retrieve data for the Streamlit dashboard.
    """
    # Get the last modified time of the Excel file
    excel_last_modified = get_file_last_modified_time(excel_file_path)

    # Check if there's a previous last modified time stored in session state
    if 'last_modified' not in st.session_state:
        st.session_state['last_modified'] = 0  # Initialize if not present

    # If the Excel file has been modified, show a notification
    if st.session_state['last_modified'] != excel_last_modified:
        # st.success('Data reloaded due to changes in the input file.')
        st.session_state['last_modified'] = excel_last_modified

    # Populate the database, using the file's last modified time to track changes
    populate_database(excel_last_modified)

    # # Populate the database directly
    # populate_database(excel_file_path, db_file_path)

    # Get data from the database
    capex_data = get_capex_data()
    opex_data = get_opex_data()
    electrolyser_data = get_electrolyser_data()
    cash_flow_data = get_cash_flow_data()
    pretreat_data = get_pretreat_equipment_cost_data()
    calc_electrolyser_data = electrolyser_formulae()
    calc_opex_data = opex_formulae()
    calc_cash_flow_data = cash_flow_formulae()
    calc_capex_data = capex_formulae()

    # <--- For debugging purposes. Display data using Streamlit to be sure that data has been read.--->
    st.title("Techno-Economic Assessment Dashboard")

    # First set of tabs for Default Data
    st.header("Default Data")
    default_tab1, default_tab2, default_tab3, default_tab4, default_tab5 = st.tabs([
        "CAPEX", "OPEX", "Electrolyser", "Cash Flow", "Pretreat"
    ])
    
    # Organize sections into tabs for better presentation

    # CAPEX Data
    with default_tab1:
        st.subheader("CAPEX Data")
        try:
            st.write(capex_data)
        except Exception as e:
            st.error(f"Error loading CAPEX data: {e}")
    
    # OPEX Data
    with default_tab2:
        st.subheader("OPEX Data")
        try:
            st.write(opex_data)
        except Exception as e:
            st.error(f"Error loading OPEX data: {e}")
    
    # Electrolyser Data
    with default_tab3:
        st.subheader("Electrolyser Data")
        try:
            st.write(electrolyser_data)
        except Exception as e:
            st.error(f"Error loading Electrolyser data: {e}")
    
    # Cash Flow Data
    with default_tab4:
        st.subheader("Cash Flow Data")
        try:
            st.write(cash_flow_data)
        except Exception as e:
            st.error(f"Error loading Cash Flow data: {e}")
    
    # Pretreat Data
    with default_tab5:
        st.subheader("Pretreat Data")
        try:
            st.write(pretreat_data)
        except Exception as e:
            st.error(f"Error loading Pretreat data: {e}")
    
    # Second set of tabs for Calculated Data
    st.header("Calculated Data")
    calc_tab1, calc_tab2, calc_tab3, calc_tab4 = st.tabs([
        "Calculated CAPEX", "Calculated OPEX", "Calculated Electrolyser", "Calculated Cash Flow"
    ])
    
    # Calculated CAPEX Data
    with calc_tab1:
        st.subheader("Calculated CAPEX Data")
        try:
            st.write(calc_capex_data)
        except Exception as e:
            st.error(f"Error calculating CAPEX: {e}")
    
    # Calculated OPEX Data
    with calc_tab2:
        st.header("Calculated OPEX Data")
        try:
            st.write(calc_opex_data)
        except Exception as e:
            st.error(f"Error calculating OPEX: {e}")
    
    # Calculated Electrolyser Data
    with calc_tab3:
        st.subheader("Calculated Electrolyser Data")
        try:
            st.write(calc_electrolyser_data)
        except Exception as e:
            st.error(f"Error calculating Electrolyser data: {e}")
    
    # Calculated Cash Flow Data
    with calc_tab4:
        st.subheader("Calculated Cash Flow Data")
        try:
            st.write(calc_cash_flow_data)
        except Exception as e:
            st.error(f"Error calculating Cash Flow: {e}")
    

    # Discounted Cash Flow Analysis Section
    st.header("Discounted Cash Flow Analysis")

    # Run the discounted cash flow analysis
    try:
        dcf_result = discounted_cash_flow_analysis()
        st.subheader("Discounted Cash Flow Values ($M)")
        st.dataframe(dcf_result.T)

        # Plot the Cumulative NPV
        st.subheader("Cumulative Net Present Value (NPV) Over Time")
        st.line_chart(dcf_result[['Year', 'Cumulative NPV']].set_index('Year'))
    except Exception as e:
        st.error(f"Error calculating Discounted Cash Flow Analysis: {e}")

if __name__ == "__main__":
    main()
