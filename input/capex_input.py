import sqlite3
import pandas as pd

def get_capex_data():
    """
    Fetches CAPEX data from the SQLite database and returns key CAPEX variables for computation.
    
    Parameters:
    ----------
    None
    
    Returns:
    -------
    tuple
        A tuple containing the following variables retrieved from the CAPEX data:
        - install_cost (float): Installation cost. Defaults to 0 if the key is not found.
        - controls_and_instrumentation (float): Cost of controls and instrumentation. Defaults to 0 if the key is not found.
        - piping_and_electricals (float): Cost of piping and electricals. Defaults to 0 if the key is not found.
        - building_and_services (float): Cost of building and services. Defaults to 0 if the key is not found.
        - indirect_cost (float): Indirect cost. Defaults to 0 if the key is not found.
        - startup_cost (float): Startup cost. Defaults to 0 if the key is not found.
        - working_capital (float): Working capital. Defaults to 0 if the key is not found.
    
    Database Connection:
    -------------------
    - Connects to the SQLite database located at 'data/database.db' and retrieves the 'capex_factors' table.
    
    Debugging:
    ---------
    - Prints the DataFrame fetched from the database for verification.
    - Prints the keys of the dictionary after converting the DataFrame to ensure proper formatting.
    - If a key is not found when attempting to retrieve a value, a warning message is printed, and a default value is used.
    """
    db_file_path = 'data/database.db'
    query = "SELECT * FROM capex_factors"
    
    with sqlite3.connect(db_file_path) as conn:
        capex_data = pd.read_sql_query(query, conn)
    
    # Print the data to debug if the key exists
    print(capex_data)

    # Convert the DataFrame to a dictionary, normalizing the keys to lowercase and stripping all spaces
    capex_factors_data_dict = capex_data.set_index(capex_data['Category'].str.replace(' ', '').str.lower())['Value'].to_dict()
    
    # Print dictionary keys for debugging
    print(capex_factors_data_dict.keys())
    
    def get_value(key, default=None):
        """
        Safely retrieves a value from the CAPEX dictionary using a normalized key.
        
        Parameters:
        ----------
        key : str
            The key to search for in the dictionary. It is normalized to lowercase and spaces are removed for consistent access.
        
        default : any, optional
            The default value to return if the key is not found. Defaults to None.
        
        Returns:
        -------
        float
            The value associated with the given key in the CAPEX dictionary, or the default value if the key is not found.
        """
        try:
            return capex_factors_data_dict[key.replace(' ', '').strip().lower()]  # Normalize key access
        except KeyError:
            print(f"Warning: '{key}' not found in the data. Using default value: {default}")
            return default

    # Retrieve variables with safe access
    install_cost = get_value('installation', default=0)
    controls_and_instrumentation = get_value('controls_and_instrumentation', default=0)
    piping_and_electricals = get_value('piping_and_electricals', default=0)
    building_and_services = get_value('building_and_services', default=0)
    indirect_cost = get_value('indirect_cost', default=0)
    startup_cost = get_value('startup_cost', default=0)
    working_capital = get_value('working_capital', default=0)
    
    # Return the variables
    return (
        install_cost,
        controls_and_instrumentation,
        piping_and_electricals,
        building_and_services,
        indirect_cost,
        startup_cost,
        working_capital
    )
