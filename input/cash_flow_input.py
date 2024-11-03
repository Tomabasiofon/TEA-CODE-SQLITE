import sqlite3
import pandas as pd

def get_cash_flow_data():
    """
    Fetches Cash Flow data from the SQLite database and returns key cash flow variables for computation.
    
    Parameters:
    ----------
    None
    
    Returns:
    -------
    tuple
        A tuple containing the following variables retrieved from the cash flow data:
        - tax_rate (float): The tax rate applied. Defaults to 0 if the key is not found.
        - discount_rate (float): The discount rate used in calculations. Defaults to 0 if the key is not found.
        - water_cost_price (float): The cost price of water. Defaults to 0 if the key is not found.
        - water_selling_price (float): The selling price of water. Defaults to 0 if the key is not found.
        - ammonia_selling_price (float): The selling price of ammonia. Defaults to 0 if the key is not found.
        - chemical_selling_price (float): The selling price of chemicals. Defaults to 0 if the key is not found.
        - depreciation_time (int): The time period for depreciation in years. Defaults to 0 if the key is not found.
        - life_of_plant (int): The operational life of the plant in years. Defaults to 0 if the key is not found.
        - land (float): The cost associated with land. Defaults to 0 if the key is not found.
    
    Database Connection:
    -------------------
    - Connects to the SQLite database located at 'data/database.db' and retrieves the 'cash_flow' table.
    
    Debugging:
    ---------
    - Prints the DataFrame fetched from the database for verification.
    - Prints the keys of the dictionary after converting the DataFrame to ensure proper formatting.
    - If a key is not found when attempting to retrieve a value, a warning message is printed, and a default value is used.
    """
    db_file_path = 'data/database.db'
    query = "SELECT * FROM cash_flow"
    
    with sqlite3.connect(db_file_path) as conn:
        cash_flow_data = pd.read_sql_query(query, conn)
    
    # Print the data to debug if the key exists
    print(cash_flow_data)

    # Convert the DataFrame to a dictionary, normalizing the keys to lowercase and stripping all spaces
    cash_flow_data_dict = cash_flow_data.set_index(cash_flow_data['Category'].str.replace(' ', '').str.lower())['Value'].to_dict()
    
    # Print dictionary keys for debugging
    print(cash_flow_data_dict.keys())
    
    def get_value(key, default=None):
        """
        Safely retrieves a value from the cash flow dictionary using a normalized key.
        
        Parameters:
        ----------
        key : str
            The key to search for in the dictionary. It is normalized to lowercase and spaces are removed for consistent access.
        
        default : any, optional
            The default value to return if the key is not found. Defaults to None.
        
        Returns:
        -------
        float
            The value associated with the given key in the cash flow dictionary, or the default value if the key is not found.
        """
        try:
            return cash_flow_data_dict[key.replace(' ', '').strip().lower()]  # Normalize key access
        except KeyError:
            print(f"Warning: '{key}' not found in the data. Using default value: {default}")
            return default

    # Retrieve variables with safe access
    tax_rate = get_value('tax_rate', default=0)
    discount_rate = get_value('discount_rate', default=0)
    water_selling_price = get_value('water_selling_price', default=0)
    ammonia_selling_price = get_value('ammonia_selling_price', default=0)
    chemical_selling_price = get_value('chemical_selling_price', default=0)
    water_cost_price = get_value('water_cost_price', default=0)
    depreciation_time = get_value('depreciation_time', default=0)
    life_of_plant = get_value('life_of_plant', default=0)
    land = get_value('land', default=0)
    treated_water_quantity = get_value('treated_water_quantity', default=0)
    
    # Return the variables
    return (
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
    )
