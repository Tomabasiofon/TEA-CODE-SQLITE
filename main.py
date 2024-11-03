import os
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
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

# Set Streamlit page configuration to wide layout
st.set_page_config(
    page_title="Techno-Economic Assessment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to set container width to 90% of the screen width
st.markdown(
    """
    <style>
    .main {
        max-width: 90%;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define paths
excel_file_path = 'data/input.xlsx'
db_file_path = 'data/database.db'

def get_file_last_modified_time(filepath):
    """Get the last modified time of the file to track changes."""
    return os.path.getmtime(filepath)

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
        st.session_state['last_modified'] = excel_last_modified

    # Populate the database, using the file's last modified time to track changes
    populate_database(excel_last_modified)

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

    # Display the main title
    st.title("Techno-Economic Assessment Dashboard")

    # Add a horizontal line before the Default Data section
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Default Data")
    default_tab1, default_tab2, default_tab3, default_tab4, default_tab5 = st.tabs([
        "CAPEX", "OPEX", "Electrolyser", "Cash Flow", "Pretreat"
    ])
    
    with default_tab1:
        st.subheader("CAPEX Data")
        try:
            st.write(capex_data)
        except Exception as e:
            st.error(f"Error loading CAPEX data: {e}")
    
    with default_tab2:
        st.subheader("OPEX Data")
        try:
            st.write(opex_data)
        except Exception as e:
            st.error(f"Error loading OPEX data: {e}")
    
    with default_tab3:
        st.subheader("Electrolyser Data")
        try:
            st.write(electrolyser_data)
        except Exception as e:
            st.error(f"Error loading Electrolyser data: {e}")
    
    with default_tab4:
        st.subheader("Cash Flow Data")
        try:
            st.write(cash_flow_data)
        except Exception as e:
            st.error(f"Error loading Cash Flow data: {e}")
    
    with default_tab5:
        st.subheader("Pretreat Data")
        try:
            st.write(pretreat_data)
        except Exception as e:
            st.error(f"Error loading Pretreat data: {e}")

    # Add a horizontal line before the Calculated Data section
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Calculated Data")
    calc_tab1, calc_tab2, calc_tab3, calc_tab4 = st.tabs([
        "Calculated CAPEX", "Calculated OPEX", "Calculated Electrolyser", "Calculated Cash Flow"
    ])
    
    with calc_tab1:
        st.subheader("Calculated CAPEX Data")
        try:
            st.write(calc_capex_data)
        except Exception as e:
            st.error(f"Error calculating CAPEX: {e}")
    
    with calc_tab2:
        st.subheader("Calculated OPEX Data")
        try:
            st.write(calc_opex_data)
        except Exception as e:
            st.error(f"Error calculating OPEX: {e}")
    
    with calc_tab3:
        st.subheader("Calculated Electrolyser Data")
        try:
            st.write(calc_electrolyser_data)
        except Exception as e:
            st.error(f"Error calculating Electrolyser data: {e}")
    
    with calc_tab4:
        st.subheader("Calculated Cash Flow Data")
        try:
            st.write(calc_cash_flow_data)
        except Exception as e:
            st.error(f"Error calculating Cash Flow: {e}")

    # Add a horizontal line before the Discounted Cash Flow section
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Discounted Cash Flow Analysis")

    # Retrieve the initial discount rate from cash_flow_data
    _, initial_discount_rate, _, _, _, _, _, _, _, _ = cash_flow_data

    # Run the discounted cash flow analysis using the original discount rate
    try:
        dcf_result = discounted_cash_flow_analysis(initial_discount_rate)
        st.subheader("Discounted Cash Flow Values ($M)")
        st.dataframe(dcf_result.T)

        # Plot the Cumulative NPV for various discount rates using Plotly
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Cumulative Net Present Value (NPV) Over Time at Varying Discount Rates")

       # Generate a range of discount rates from -30% to +30% of the initial rate in 10% increments
        discount_rates = [initial_discount_rate + (initial_discount_rate * i * 0.1) for i in range(-3, 4)]
        cumulative_npvs = {}
        for rate in discount_rates:
            try:
                dcf_result = discounted_cash_flow_analysis(rate)  # No division by 100 needed
                cumulative_npvs[f"{rate:.2f}%"] = dcf_result['Cumulative NPV']  # Label as percentage without extra scaling
            except Exception as e:
                st.error(f"Error calculating DCF at {rate:.2f}% discount rate: {e}")
                continue

        # Prepare data for Plotly
        fig = go.Figure()
        years = dcf_result['Year']
        for rate_label, npv in cumulative_npvs.items():
            line_width = 4 if rate_label == f"{initial_discount_rate:.2f}%" else 2
            fig.add_trace(go.Scatter(
                x=years, y=npv, mode='lines', 
                name=f"<b>{rate_label} (Original)</b>" if line_width == 4 else rate_label,
                line=dict(width=line_width)
            ))

        fig.update_layout(
            title="Cumulative NPV over Time at Different Discount Rates",
            xaxis_title="Years",
            yaxis_title="Cumulative NPV ($M)",
            legend_title="Discount Rates",
            template="plotly_white"
        )
        st.plotly_chart(fig)


    except Exception as e:
        st.error(f"Error calculating Discounted Cash Flow Analysis: {e}")

if __name__ == "__main__":
    main()
