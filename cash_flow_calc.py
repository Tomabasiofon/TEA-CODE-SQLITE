# Import the functions from the necessary modules
from input.cash_flow_input import get_cash_flow_data
from input.capex_input import get_capex_data
from electrolyser_calc import electrolyser_formulae
from input.electrolyser_input import get_electrolyser_data
from input.pretreat import get_pretreat_equipment_cost_data
from capex_calc import capex_formulae

def cash_flow_formulae(water_selling_price):
    """
    This function contains all formulae for computing additional inputs to the TEA model.
    It first reads all the variables needed for additional computation.
    Note that this computation will be done in Python, rather than Excel since the user will be provided 
    with the flexibility to manipulate the values.

    Parameters:
    ----------
    water_selling_price (float): The price of water, which can be varied for sensitivity analysis.

    Returns:
    -------
    tuple
        A tuple containing the calculated financial values needed for DCF analysis.
    """
    # Call the function to retrieve the additional data needed for computation (capex, cash flow, raw data and calculated data)
    pretreat_pec = get_pretreat_equipment_cost_data()

    (
        install_cost,
        controls_and_instrumentation,
        piping_and_electricals,
        building_and_services,
        indirect_cost,
        startup_cost,
        working_capital
    ) = get_capex_data()

    (
        tax_rate,
        discount_rate,
        water_cost_price,
        _,
        ammonia_selling_price,
        chemical_selling_price,
        depreciation_time,
        life_of_plant,
        land,
        treated_water_quantity
    ) = get_cash_flow_data()

    (
        install_cost_total,
        controls_and_instrumentation_total,
        piping_and_electricals_total,
        building_and_services_total,
        indirect_cost_total,
        direct_cost,
        fixed_capital_investment,
        startup_cost_total,
        working_capital_total,
        capex,
        total_capital_cost
    ) = capex_formulae()

    (
        current,
        kg_per_year,
        energy_consumed_kWh_kg,
        power_consumed_kW,
        total_reactor_cost,
        b_o_p,
        cat_cost,
        total_electrolyer_capital_cost,
        electrolyser_pec,
        total_electrolyer_capital_cost,
        total_electricity_cost,
        electrolyer_opex,
        electrolyser_foc,
        electrolyser_voc
    ) = electrolyser_formulae()

    (
        faradaic_constant,
        time,
        no_of_electrons,
        faradaic_efficiency,
        molar_weight,
        capacity,
        capacity_factor,
        current_density,
        reactor_cost,
        e_cell,
        balance_of_plant,
        maintenance_frequency,
        maintenance_factor,
        catalyst_percentage,
        catalyst_lifespan,
        capacity_factor,
        electrolyser_installation_cost,
        separation_cost
    ) = get_electrolyser_data()

    # Calculate financial metrics based on provided and retrieved values
    land_cost = (land * fixed_capital_investment) / 100
    total_capital_investment = fixed_capital_investment + land_cost + working_capital_total
    depreciation = total_capital_cost / depreciation_time
    total_pec = pretreat_pec + electrolyser_pec

    # Calculate revenue based on the dynamic water_selling_price parameter
    water_revenue = water_selling_price * treated_water_quantity * capacity_factor
    ammonia_revenue = ammonia_selling_price * (capacity / time) * capacity_factor
    total_revenue = water_revenue + ammonia_revenue

    # Return the calculated financial metrics
    return (
        round(land_cost, 2),
        round(total_capital_investment, 2),
        round(depreciation, 2),
        round(total_pec, 2),
        round(working_capital_total),
        round(total_revenue),
        round(water_revenue),
        round(ammonia_revenue)
    )

if __name__ == "__main__":
    # Example usage of the modified function with a sample water selling price
    water_selling_price = 1.0  # Example value
    print(cash_flow_formulae(water_selling_price))
