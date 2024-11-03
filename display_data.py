import streamlit as st

def display_default_data(capex_data, opex_data, electrolyser_data, cash_flow_data, pretreat_data):
    """
    Displays the Default Data section in Streamlit with separate tabs for each data category.
    
    Parameters:
    -----------
    capex_data : DataFrame
        The capital expenditure (CAPEX) data to be displayed.
    opex_data : DataFrame
        The operational expenditure (OPEX) data to be displayed.
    electrolyser_data : DataFrame
        The electrolyser data to be displayed.
    cash_flow_data : DataFrame
        The cash flow data to be displayed.
    pretreat_data : DataFrame
        The pretreatment equipment cost data to be displayed.
    
    Returns:
    --------
    None
        This function displays the provided data in an organized tabbed format within Streamlit.
    
    Notes:
    ------
    Each category of data is displayed in a separate tab for better organization and readability.
    Errors in loading data are displayed as error messages within each tab.
    """
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

def display_calculated_data(calc_capex_data, calc_opex_data, calc_electrolyser_data, calc_cash_flow_data):
    """
    Displays the Calculated Data section in Streamlit with separate tabs for each calculated data category.
    
    Parameters:
    -----------
    calc_capex_data : DataFrame
        The calculated capital expenditure (CAPEX) data to be displayed.
    calc_opex_data : DataFrame
        The calculated operational expenditure (OPEX) data to be displayed.
    calc_electrolyser_data : DataFrame
        The calculated electrolyser data to be displayed.
    calc_cash_flow_data : DataFrame
        The calculated cash flow data to be displayed.
    
    Returns:
    --------
    None
        This function displays the provided calculated data in an organized tabbed format within Streamlit.
    
    Notes:
    ------
    Each calculated data category is displayed in a separate tab for better organization and readability.
    Errors in calculations are displayed as error messages within each tab.
    """
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
