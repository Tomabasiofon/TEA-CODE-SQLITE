from opex_calc import opex_formulae

def see ():

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

if __name__ == "__main__":
    opex_formulae()