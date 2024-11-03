import sqlite3
import pandas as pd

def get_electrolyser_data():
    """
    Fetches Electrolyser data from the SQLite database and returns key electrolyser variables for computation.
    
    Parameters:
    ----------
    None
    
    Returns:
    -------
    tuple
        A tuple containing the following variables retrieved from the electrolyser data:
        - faradaic_constant (float): Faradaic constant value. Defaults to 0 if the key is not found.
        - time (float): Time duration for electrolysis. Defaults to 0 if the key is not found.
        - no_of_electrons (int): Number of electrons involved in the reaction. Defaults to 0 if the key is not found.
        - faradaic_efficiency (float): Efficiency of the electrolysis process. Defaults to 0 if the key is not found.
        - molar_weight (float): Molar weight of the product. Defaults to 0 if the key is not found.
        - capacity (float): Capacity of the electrolyser. Defaults to 0 if the key is not found.
        - current_density (float): Current density used in the electrolyser. Defaults to 0 if the key is not found.
        - reactor_cost (float): Cost of the reactor. Defaults to 0 if the key is not found.
        - e_cell (float): Voltage of the electrolytic cell. Defaults to 0 if the key is not found.
        - balance_of_plant (float): Cost of the balance of plant. Defaults to 0 if the key is not found.
        - maintenance_frequency (int): Frequency of maintenance required. Defaults to 0 if the key is not found.
        - maintenance_factor (float): Maintenance factor applied. Defaults to 0 if the key is not found.
        - catalyst_percentage (float): Percentage of catalyst used. Defaults to 0 if the key is not found.
        - catalyst_lifespan (float): Lifespan of the catalyst in years. Defaults to 0 if the key is not found.
        - capacity_factor (float): Capacity factor of the electrolyser. Defaults to 0 if the key is not found.
        - electrolyser_installation_cost (float): Installation cost of the electrolyser. Defaults to 0 if the key is not found.
        - separation_cost (float): Cost for separation processes. Defaults to 0 if the key is not found.
    
    Database Connection:
    -------------------
    - Connects to the SQLite database located at 'data/database.db' and retrieves the 'electrolyser' table.
    
    Debugging:
    ---------
    - Prints the DataFrame fetched from the database for verification.
    - Prints the keys of the dictionary after converting the DataFrame to ensure proper formatting.
    - If a key is not found when attempting to retrieve a value, a warning message is printed, and a default value is used.
    """
    db_file_path = 'data/database.db'
    query = "SELECT * FROM electrolyser"
    
    with sqlite3.connect(db_file_path) as conn:
        electrolyser_data = pd.read_sql_query(query, conn)
    
    # Print the data to debug if the key exists
    print(electrolyser_data)

    # Convert the DataFrame to a dictionary, normalizing the keys to lowercase and stripping whitespace
    electrolyser_data_dict = electrolyser_data.set_index(electrolyser_data['Category'].str.replace(' ', '').str.lower())['Value'].to_dict()
    
    # Print dictionary keys for debugging
    print(electrolyser_data_dict.keys())
    
    def get_value(key, default=None):
        """
        Safely retrieves a value from the electrolyser dictionary using a normalized key.
        
        Parameters:
        ----------
        key : str
            The key to search for in the dictionary. It is normalized to lowercase and spaces are removed for consistent access.
        
        default : any, optional
            The default value to return if the key is not found. Defaults to None.
        
        Returns:
        -------
        float
            The value associated with the given key in the electrolyser dictionary, or the default value if the key is not found.
        """
        try:
            return electrolyser_data_dict[key.replace(' ', '').strip().lower()]  # Normalize key access
        except KeyError:
            print(f"Warning: '{key}' not found in the data. Using default value: {default}")
            return default

    # Retrieve variables with safe access
    faradaic_constant = get_value('faradaic_constant', default=0)
    time = get_value('time', default=0)
    no_of_electrons = get_value('no_of_electrons', default=0)
    faradaic_efficiency = get_value('faradaic_efficiency', default=0)
    molar_weight = get_value('molar_weight', default=0)
    capacity = get_value('capacity', default=0)
    current_density = get_value('current_density', default=0)
    reactor_cost = get_value('reactor_cost', default=0)
    e_cell = get_value('e_cell', default=0)
    balance_of_plant = get_value('balance_of_plant', default=0)
    maintenance_frequency = get_value('maintenance_frequency', default=0)  # Correctly retrieved now
    maintenance_factor = get_value('maintenance_factor', default=0)
    catalyst_percentage = get_value('catalyst_percentage', default=0)
    catalyst_lifespan = get_value('catalyst_lifespan', default=0)
    capacity_factor = get_value('capacity_factor', default=0)
    electrolyser_installation_cost = get_value('electrolyser_installation_cost', default=0)
    separation_cost = get_value('separation_cost', default=0)
    
    # Return the variables along with the full data
    return (
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
    )
