import os
import streamlit as st
import numpy as np
import pandas as pd

# Import the functions from the necessary modules
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

def discounted_cash_flow_analysis(discount_rate):
    """
    Performs a discounted cash flow (DCF) analysis to assess the profitability of a project
    over its lifespan by considering revenue, costs, taxes, and discounting cash flows.

    Parameters:
        discount_rate (float): The discount rate to apply for NPV calculations.

    Returns:
        pd.DataFrame: A DataFrame containing calculated DCF values, including NPV and cumulative NPV.
    """

    # Retrieve parameters from cash_flow_calc module
    (
        land_cost,
        total_capital_investment,
        depreciation,
        total_pec,
        working_capital_total,
        total_revenue,
        water_revenue,
        ammonia_revenue
    ) = cash_flow_formulae()

    # Retrieve the operating expense (opex) from opex_calc module
    (
        labour_cost,
        supervision_cost,
        direct_overhead_cost,
        general_overhead_cost,
        insurance_cost,
        miscellaneous_cost,
        laboratory_cost_total,
        working_capital_financing_cost,
        opex
    ) = opex_formulae()

    # Retrieve tax rate and other financial parameters from cash_flow_input module
    (
        tax_rate,
        _,
        water_cost_price,
        water_selling_price,
        ammonia_selling_price,
        chemical_selling_price,
        depreciation_time,
        life_of_plant,
        land,
        treated_water_quantity
    ) = get_cash_flow_data()

    # Setting up the analysis period (0 to 20 years)
    years = np.arange(0, 21)

    # Calculate initial investment values across specified years
    initial_investment = np.zeros(len(years))
    initial_investment[0] = 0.5 * total_capital_investment + land_cost
    initial_investment[1] = 0.5 * total_capital_investment + working_capital_total
    initial_investment[-1] = -(land_cost + working_capital_total)

    # Operating cost remains constant from year 2 onward
    operating_cost = np.zeros(len(years))
    operating_cost[2:] = opex

    # Revenue initialization, partial for year 2, full from year 3
    revenue = np.zeros(len(years))
    revenue[2] = (2 / 3) * total_revenue  # Two-thirds of revenue in year 2
    revenue[3:] = total_revenue  # Full revenue from year 3 onward

    # Depreciation values applied from year 2 to year 16
    depreciation_values = np.zeros(len(years))
    depreciation_values[2:17] = depreciation

    # Create DataFrame for cash flow calculations
    discounted_cash_flow_values = pd.DataFrame({
        'Year': years,
        'Annual Investment': initial_investment,
        'Operating Cost': operating_cost,
        'Revenue': revenue,
        'Depreciation': depreciation_values
    })

    # Calculate Net Profit Before Taxes for each year
    discounted_cash_flow_values['Net Profit Before Taxes'] = (
        discounted_cash_flow_values['Revenue'] - 
        discounted_cash_flow_values['Operating Cost'] - 
        discounted_cash_flow_values['Depreciation'] - 
        discounted_cash_flow_values['Annual Investment']
    )

    # Calculate Federal Income Tax based on tax rate
    federal_income_tax = np.zeros(len(years))
    federal_income_tax[2:] = (tax_rate/100) * discounted_cash_flow_values['Net Profit Before Taxes'][2:]
    discounted_cash_flow_values['Federal Income Tax'] = federal_income_tax

    # Calculate Net Profit After Taxes
    discounted_cash_flow_values['Net Profit After Taxes'] = (
        discounted_cash_flow_values['Net Profit Before Taxes'] - 
        discounted_cash_flow_values['Federal Income Tax']
    )

    # Calculate Free Cash Flow (including depreciation)
    discounted_cash_flow_values['Free Cash Flow'] = (
        discounted_cash_flow_values['Net Profit After Taxes'] + 
        discounted_cash_flow_values['Depreciation']
    )

    # Calculate Cumulative Cash Flow as the cumulative sum of Free Cash Flow
    discounted_cash_flow_values['Cumulative Cash Flow'] = discounted_cash_flow_values['Free Cash Flow'].cumsum()

    # Calculate Net Present Value (NPV) for each year using the passed-in discount rate
    discounted_cash_flow_values['Net Present Value (NPV)'] = (
        discounted_cash_flow_values['Free Cash Flow'] / ((1 + (discount_rate/100)) ** (discounted_cash_flow_values['Year']))
    )

    # Calculate Cumulative NPV
    discounted_cash_flow_values['Cumulative NPV'] = discounted_cash_flow_values['Net Present Value (NPV)'].cumsum()

    # Normalize all monetary values by dividing by 1,000,000
    discounted_cash_flow_values.iloc[:, 1:] /= 1_000_000

    # Round all monetary values to 2 decimal places
    discounted_cash_flow_values.iloc[:, 1:] = discounted_cash_flow_values.iloc[:, 1:].round(2)

    return discounted_cash_flow_values


if __name__ == "__main__":
    # Example usage: Run DCF analysis with a specified discount rate
    discounted_cash_flow_analysis(discount_rate)
