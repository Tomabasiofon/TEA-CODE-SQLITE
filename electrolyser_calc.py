
# Import the get_electrolyser_data function from the input.electrolyser_input module
from input.electrolyser_input import get_electrolyser_data
from input.opex_input import get_opex_data

def electrolyser_formulae():
    """
    This function contains all formulae for computing additional inputs to the TEA model.
    It first reads all the variables needed for additional computauion.
    Note that this computations will be done in python, rather than excel since the user will be provided with the flexibility to manipulate the values.
    """
    # Call the function to retrieve the data (electrolyser and opex data since we need it for calculation)
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

    # Print values for debugging
    print("Faradaic Constant:", faradaic_constant)
    print("Time:", time)
    print("Number of Electrons:", no_of_electrons)
    print("Faradaic Efficiency:", faradaic_efficiency)
    print("Molar Weight:", molar_weight)
    print("Capacity:", capacity)
    print("Current Density:", current_density)
    print("Reactor Cost:", reactor_cost)
    print("E Cell:", e_cell)
    print("Balance of Plant:", balance_of_plant)
    print("Maintenance Frequency:", maintenance_frequency)
    print("Maintenance Factor:", maintenance_factor)
    print("Catalyst Percentage:", catalyst_percentage)
    print("Catalyst Lifespan:", catalyst_lifespan)
    print("Capacity Factor:", capacity_factor)
    print("Separation_cost", separation_cost)


    # Now you can use the variables as needed: Current
    current = (no_of_electrons*faradaic_constant*capacity)/(molar_weight*3600*(faradaic_efficiency/100)*time)
    
    #kg/hr to kg/year Conversion
    kg_per_year = (capacity*capacity_factor * 365)/8760

    # Energy Consumed
    energy_consumed_kWh_kg = (current*e_cell*time)/ capacity

    # Power Consumed
    power_consumed_kW = (current*e_cell)/1000

    # Reactor Area
    electrolyser_area_m2 = current/current_density

    #Reactor Cost
    total_reactor_cost = reactor_cost* electrolyser_area_m2

    #electrolyser installation cost
    total_electrolyser_installation =  (electrolyser_installation_cost * total_reactor_cost)/100


    # Balance of Plant
    b_o_p = (balance_of_plant * total_reactor_cost)/100

    #Catalyst Cost
    cat_cost_per_kg = ((total_reactor_cost * (catalyst_percentage / 100))/(0.345 * catalyst_lifespan * 365 * capacity))
    cat_cost = cat_cost_per_kg * kg_per_year

    # Electrolyser PEC
    electrolyser_pec = total_reactor_cost + b_o_p

    # Total Capital cost from electrolyser
    total_electrolyer_capital_cost = electrolyser_pec + total_electrolyser_installation

    

    maintenance_cost = (maintenance_frequency * maintenance_factor * total_electrolyer_capital_cost)/100

    electricity_cost_per_kg = (power_consumed_kW * electricity_unit_cost * 24)/capacity

    total_electricity_cost = electricity_cost_per_kg * kg_per_year

    total_separation_cost = (separation_cost * total_electricity_cost)/100

    electrolyser_voc = total_electricity_cost + cat_cost

    electrolyser_foc = total_separation_cost + maintenance_cost

    electrolyer_opex = electrolyser_voc + electrolyser_foc

    return (
        round(current, 2),
        round(kg_per_year, 2),
        round(energy_consumed_kWh_kg, 2),
        round(power_consumed_kW, 2),
        round(total_reactor_cost, 2),
        round(b_o_p, 2),
        round(cat_cost, 2),
        round(total_electrolyer_capital_cost, 2),
        round(electrolyser_pec, 2),
        round(total_electrolyer_capital_cost, 2),
        round(total_electricity_cost, 2),
        round(electrolyer_opex, 2),
        round(electrolyser_foc, 2),
        round(electrolyser_voc, 2)
    )


if __name__ == "__main__":
    electrolyser_formulae()

    