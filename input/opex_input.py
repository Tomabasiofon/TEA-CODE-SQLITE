import sqlite3
import pandas as pd

def get_opex_data():
    """
    Fetches OPEX (Operating Expenditure) data from the SQLite database and returns key OPEX variables for computation.
    
    Parameters:
    ----------
    None
    
    Returns:
    -------
    tuple
        A tuple containing the following variables retrieved from the OPEX data:
        - base_labour_wage (float): The base wage for labourers. Defaults to 0 if the key is not found.
        - no_of_labourers (int): Number of labourers. Defaults to 0 if the key is not found.
        - supervision (float): Cost associated with supervision. Defaults to 0 if the key is not found.
        - direct_overhead (float): Cost of direct overhead. Defaults to 0 if the key is not found.
        - general_overhead (float): Cost of general overhead. Defaults to 0 if the key is not found.
        - insurance (float): Insurance cost. Defaults to 0 if the key is not found.
        - miscellaneous (float): Miscellaneous expenses. Defaults to 0 if the key is not found.
        - laboratory_cost (float): Laboratory costs associated with operations. Defaults to 0 if the key is not found.
        - working_capital_financing (float): Cost of financing working capital. Defaults to 0 if the key is not found.
        - electricity_unit_cost (float): Unit cost of electricity. Defaults to 0 if the key is not found.
        - raw_material (float): Cost of raw materials. Defaults to 0 if the key is not found.
        - pump_power (float): Power usage for pumps. Defaults to 0 if the key is not found.
    
    Database Connection:
    -------------------
    - Connects to the SQLite database located at 'data/database.db' and retrieves the 'opex_factors' table.
    
    Debugging:
    ---------
    - Prints the DataFrame fetched from the database for verification.
    - Prints the keys of the dictionary after converting the DataFrame to ensure proper formatting.
    - If a key is not found when attempting to retrieve a value, a warning message is printed, and a default value is used.
    """
    db_file_path = 'data/database.db'
    query = "SELECT * FROM opex_factors"
    
    with sqlite3.connect(db_file_path) as conn:
        opex_data = pd.read_sql_query(query, conn)

    # Print the data to debug if the key exists
    print(opex_data)

    # Convert the DataFrame to a dictionary, normalizing the keys to lowercase and stripping all spaces
    opex_factors_data_dict = opex_data.set_index(opex_data['Category'].str.replace(' ', '').str.lower())['Value'].to_dict()
    
    # Print dictionary keys for debugging
    print(opex_factors_data_dict.keys())
    
    def get_value(key, default=None):
        """
        Safely retrieves a value from the OPEX dictionary using a normalized key.
        
        Parameters:
        ----------
        key : str
            The key to search for in the dictionary. It is normalized to lowercase and spaces are removed for consistent access.
        
        default : any, optional
            The default value to return if the key is not found. Defaults to None.
        
        Returns:
        -------
        float
            The value associated with the given key in the OPEX dictionary, or the default value if the key is not found.
        """
        try:
            return opex_factors_data_dict[key.replace(' ', '').strip().lower()]  # Normalize key access
        except KeyError:
            print(f"Warning: '{key}' not found in the data. Using default value: {default}")
            return default

    # Retrieve variables with safe access
    base_labour_wage = get_value('base_labour_wage', default=0)
    no_of_labourers = get_value('no_of_labourers', default=0)
    supervision = get_value('supervision', default=0)
    direct_overhead = get_value('direct_overhead', default=0)
    general_overhead = get_value('general_overhead', default=0)
    insurance = get_value('insurance', default=0)
    miscellaneous = get_value('miscellaneous', default=0)
    laboratory_cost = get_value('laboratory_cost', default=0)
    working_capital_financing = get_value('working_capital_financing', default=0)
    electricity_unit_cost = get_value('electricity_unit_cost', default=0)
    raw_material = get_value('raw_material', default=0)
    pump_power = get_value('pump_power', default=0)
    chemical_cost = get_value('chemical_cost',default=0)
    chemical_quantity = get_value('chemical_quantity', default=0)
    
    # Return the variables
    return (
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
    )
