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
from display_data import display_default_data, display_calculated_data

# Set Streamlit page configuration to wide layout
st.set_page_config(
    page_title="Techno-Economic Assessment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to set container width to 90% of the screen width and add sidebar border and spacing
st.markdown(
    """
    <style>
    .main {
        max-width: 90%;
        margin: 0 auto;
    }
    /* Style for right border and spacing in the sidebar */
    .css-1d391kg {  
        border-right: 3px solid #ffffff;
        padding-right: 15px;
    }
    /* Horizontal line styling */
    .sidebar-divider {
        border-top: 1px solid #cccccc;
        margin-top: 15px;
        margin-bottom: 15px;
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
    # Main Title
    st.title("Techno-Economic Assessment Dashboard")

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

    # Display Default Data
    display_default_data(capex_data, opex_data, electrolyser_data, cash_flow_data, pretreat_data)

    # Display Calculated Data
    display_calculated_data(calc_capex_data, calc_opex_data, calc_electrolyser_data, calc_cash_flow_data)

    # Add a horizontal line before the Discounted Cash Flow section
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Discounted Cash Flow Analysis")

    # Retrieve the initial discount rate and tax rate from cash_flow_data
    _, initial_discount_rate, _, _, _, _, _, _, _, _ = cash_flow_data
    tax_rate, *_ = cash_flow_data  # Assuming tax_rate is the first item in cash_flow_data

    # Sidebar header for Parameter Sensitivity
    st.sidebar.header("Parameter Sensitivity")
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)  # Add horizontal line after header

    # Grouped sliders for Cash Flow Rate Changes
    with st.sidebar.expander("Cash Flow Rate Changes"):
        # Discount rate slider for dynamic updates
        discount_rate = st.slider(
            "Discount Rate (%)", min_value=0.0, max_value=20.0, value=initial_discount_rate, step=0.1
        )

        # Tax rate slider for dynamic updates
        tax_rate = st.slider(
            "Tax Rate (%)", min_value=0.0, max_value=50.0, value=tax_rate, step=0.5
        )
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)  # Add horizontal line after expander

    # Run the discounted cash flow analysis with dynamic discount and tax rates
    try:
        dcf_result = discounted_cash_flow_analysis(discount_rate, tax_rate)
        st.subheader("Discounted Cash Flow Values ($M)")
        st.dataframe(dcf_result.T)

        # Plot the Cumulative NPV for various discount rates using Plotly
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Cumulative Net Present Value (NPV) Over Time at Varying Discount Rates")

        # Generate a range of discount rates from -30% to +30% of the slider value in 10% increments
        discount_rates = [discount_rate + (discount_rate * i * 0.1) for i in range(-3, 4)]
        cumulative_npvs = {}
        for rate in discount_rates:
            try:
                dcf_result = discounted_cash_flow_analysis(rate, tax_rate)  # Pass tax_rate to ensure dynamic updates
                cumulative_npvs[f"{rate:.2f}%"] = dcf_result['Cumulative NPV']
            except Exception as e:
                st.error(f"Error calculating DCF at {rate:.2f}% discount rate: {e}")
                continue

        # Prepare data for Plotly
        fig = go.Figure()
        years = dcf_result['Year']
        for rate_label, npv in cumulative_npvs.items():
            line_width = 4 if rate_label == f"{discount_rate:.2f}%" else 2
            fig.add_trace(go.Scatter(
                x=years, y=npv, mode='lines',
                name=f"<b>{rate_label} (Current)</b>" if line_width == 4 else rate_label,
                line=dict(width=line_width)
            ))

        # Update layout for bold yellow horizontal line at y=0
        fig.update_layout(
            title="Cumulative NPV over Time at Different Discount Rates",
            xaxis_title="Years",
            yaxis_title="Cumulative NPV ($M)",
            legend_title="Discount Rates",
            template="plotly_white",
            shapes=[
                dict(
                    type="line",
                    x0=years.min(),
                    x1=years.max(),
                    y0=0,
                    y1=0,
                    line=dict(color="yellow", width=3)
                )
            ]
        )
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error calculating Discounted Cash Flow Analysis: {e}")

if __name__ == "__main__":
    main()
