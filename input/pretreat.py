import sqlite3
import pandas as pd

def get_pretreat_equipment_cost_data():
    """
    Fetches pretreatment equipment cost data from the SQLite database and retrieves the value for specific equipment.
    
    Parameters:
    ----------
    None
    
    Returns:
    -------
    float
        The value associated with 'pretreat_pec' from the 'Base year' column in the pretreatment equipment cost data.
        If the key is not found, it defaults to 0.
    
    Database Connection:
    -------------------
    - Connects to the SQLite database located at 'data/database.db' and retrieves the 'pretreat_equipment_cost' table.
    
    Additional Computations:
    -----------------------
    - Converts the DataFrame to a dictionary where the keys are equipment names from the 'Equipment' column,
      and the values are from the 'Base year' column for quick lookups.
    
    Debugging:
    ---------
    - If a key ('pretreat_pec') is not found when attempting to retrieve a value, a warning message is printed,
      and a default value of 0 is used.
    """
    db_file_path = 'data/database.db'
    query = "SELECT * FROM pretreat_equipment_cost"
    
    with sqlite3.connect(db_file_path) as conn:
        pretreat_equipment_cost_data = pd.read_sql_query(query, conn)
    
    # Convert the DataFrame to a dictionary for fast lookups
    pretreat_data_dict = pretreat_equipment_cost_data.set_index('Equipment')['Base year'].to_dict()
    
    def get_value(key, default=None):
        """
        Safely retrieves a value from the pretreatment equipment cost dictionary using the given key.
        
        Parameters:
        ----------
        key : str
            The key to search for in the dictionary (e.g., 'pretreat_pec').
        
        default : any, optional
            The default value to return if the key is not found. Defaults to None.
        
        Returns:
        -------
        float
            The value associated with the given key in the dictionary, or the default value if the key is not found.
        """
        try:
            return pretreat_data_dict[key]
        except KeyError:
            print(f"Warning: '{key}' not found in the data. Using default value: {default}")
            return default

    # Retrieve 'pretreat_pec' value with safe access
    pretreat_pec = get_value('pretreat_pec', default=0)
    
    # Return the pretreat_pec value
    return pretreat_pec

# Example usage
if __name__ == "__main__":
    pretreat_pec_value = get_pretreat_equipment_cost_data()
