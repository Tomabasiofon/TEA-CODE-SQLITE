import sqlite3
import pandas as pd

# Import necessary functions from other modules
from input.opex_input import get_opex_data
from input.capex_input import get_capex_data
from input.cash_flow_input import get_cash_flow_data
from input.pretreat import get_pretreat_equipment_cost_data
from input.electrolyser_input import get_electrolyser_data
from capex_calc import capex_formulae
from electrolyser_calc import electrolyser_formulae

def opex_formulae():
    """
    This function computes the operational expenditures (OPEX) by reading relevant variables and applying the necessary formulae.
    """

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
        base_labour_wage,
        no_of_labourers,
        supervision,
        direct_overhead,
        general_overhead,
        insurance,
        miscellaneous,
        laboratory_cost,
        working_capital_financing,
        electricity_unit_cost,
        raw_material,
        pump_power,
        chemical_cost,
        chemical_quantity
    ) = get_opex_data()


    # Call function to retrieve additional data needed
    
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
        tax_rate,
        discount_rate,
        water_cost_price,
        water_selling_price,
        ammonia_selling_price,
        chemical_selling_price,
        depreciation_time,
        life_of_plant,
        land,
        treated_water_quantity
    ) = get_cash_flow_data()


    # Labour cost
    labour_cost = base_labour_wage * no_of_labourers

    # Supervision cost
    supervision_cost = (supervision * labour_cost)/100

    # Direct overhead cost
    direct_overhead_cost = (direct_overhead * (labour_cost + supervision_cost))/100

    # General overhead cost
    general_overhead_cost = (general_overhead * (labour_cost + supervision_cost + direct_overhead_cost))/100

    # Insurance cost (based on Fixed Capital Investment (FCI))
    insurance_cost = (insurance * fixed_capital_investment)/100

    # Miscellaneous cost (based on FCI)
    miscellaneous_cost = (miscellaneous * fixed_capital_investment)/100

    # Laboratory cost
    laboratory_cost_total = (laboratory_cost * labour_cost)/100

    # Working capital financing cost
    working_capital_financing_cost = (working_capital_financing * working_capital_total)/100

    # Fixed operating cost
    fixed_operating_cost = supervision_cost + direct_overhead_cost + general_overhead_cost  + insurance_cost + miscellaneous_cost + laboratory_cost_total + working_capital_financing_cost + electrolyser_foc

    # Raw material cost
    raw_material_cost = raw_material * water_cost_price

    # Chemicals cost
    total_chemical_cost = chemical_cost * chemical_quantity * capacity_factor

    # Separatint unit Electricity Cost
    sep_unit_electricity_cost = electricity_unit_cost * pump_power * capacity_factor

    # Variable operating cost
    variable_operating_cost = sep_unit_electricity_cost + raw_material_cost + electrolyser_voc + total_chemical_cost

    # Total OpEx
    opex = fixed_operating_cost + variable_operating_cost

    # Return all computed values
    return (
        round(labour_cost, 2),
        round(supervision_cost, 2),
        round(direct_overhead_cost, 2),
        round(general_overhead_cost, 2),
        round(insurance_cost, 2),
        round(miscellaneous_cost, 2),
        round(laboratory_cost_total, 2),
        round(working_capital_financing_cost, 2),
        round(opex, 2)
    )

# Example usage
if __name__ == "__main__":
    print(opex_formulae)
    opex_formulae()