# Import the functions from the necessary modules
from input.capex_input import get_capex_data
from input.pretreat import get_pretreat_equipment_cost_data
from input.electrolyser_input import get_electrolyser_data
from electrolyser_calc import electrolyser_formulae

# Import the get_electrolyser_data function from the input.electrolyser_input module

def capex_formulae():
    """
    This function contains all formulae for computing additional inputs to the TEA model.
    It first reads all the variables needed for additional computauion.
    Note that this computations will be done in python, rather than excel since the user will be provided with the flexibility to manipulate the values.
    """
    # Call the function to retrieve the data
    pretreat_pec = get_pretreat_equipment_cost_data()

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

    # Total PEC
    total_capital_cost = pretreat_pec + electrolyser_pec
    
    (
        install_cost,
        controls_and_instrumentation,
        piping_and_electricals,
        building_and_services,
        indirect_cost,
        startup_cost,
        working_capital
    ) = get_capex_data()

    install_cost_total = (install_cost * pretreat_pec)/100
    controls_and_instrumentation_total = (controls_and_instrumentation * pretreat_pec)/100
    piping_and_electricals_total = (piping_and_electricals * pretreat_pec)/100
    building_and_services_total = (building_and_services * pretreat_pec)/100
    direct_cost = pretreat_pec + install_cost_total + controls_and_instrumentation_total + piping_and_electricals_total + building_and_services_total + total_electrolyer_capital_cost
    indirect_cost_total = (indirect_cost * direct_cost)/100
    fixed_capital_investment = direct_cost + indirect_cost_total
    startup_cost_total = (startup_cost * fixed_capital_investment)/100
    working_capital_total = (working_capital * fixed_capital_investment)/100
    capex = fixed_capital_investment + startup_cost_total + working_capital_total
    
    return (
        round(install_cost_total, 2),
        round(controls_and_instrumentation_total, 2),
        round(piping_and_electricals_total, 2),
        round(building_and_services_total, 2),
        round(indirect_cost_total, 2),
        round(direct_cost, 2),
        round(fixed_capital_investment, 2),
        round(startup_cost_total, 2),
        round(working_capital_total, 2),
        round (capex, 2),
        round(total_capital_cost,2)
    )


if __name__ == "__main__":
    capex_formulae()
