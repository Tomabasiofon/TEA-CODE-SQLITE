import pandas as pd
import sqlite3

def read_excel_data(file_path):
    """
    Reads data from an Excel file and returns a dictionary of DataFrames, one for each sheet specified.
    
    Parameters:
    ----------
    file_path : str
        The path to the Excel file (e.g., 'data/input.xlsx').
    
    Returns:
    -------
    dict
        A dictionary where the keys are the sheet names (as specified in the function) and the values are 
        pandas DataFrames containing the data from each corresponding sheet. If a sheet is not found in 
        the Excel file, it is skipped, and a message is printed for debugging purposes.
    
    Debugging:
    ---------
    - Prints messages indicating whether each specified sheet is successfully loaded or not.
    """
    sheet_names = ['capex_factors', 'opex_factors', 'electrolyser', 'cash_flow', 'pretreat_equipment_cost'] # These are the sheets holding the data.
    data_dict = {}
    
    excel_file = pd.ExcelFile(file_path)
    for sheet in sheet_names:
        if sheet in excel_file.sheet_names:
            data_dict[sheet] = pd.read_excel(file_path, sheet_name=sheet)
            # For debugging purposes.
            print(f"Loaded data from sheet '{sheet}' into the dictionary.")
        else:
            # For debugging purposes.
            print(f"Sheet '{sheet}' not found in the Excel file.")
    
    return data_dict

def create_table_from_df(df, table_name, conn):
    """
    Creates a table in the SQLite database from a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame containing data to be inserted into the database table.
        
    table_name : str
        The name of the table to create or replace in the SQLite database.
        
    conn : sqlite3.Connection
        The SQLite database connection object.
    
    Debugging:
    ---------
    - Prints a message indicating that the table has been created or replaced in the database.
    """
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    # For debugging purposes.
    print(f"Table '{table_name}' created in the SQLite database.")

def populate_db_from_excel(file_path, db_path):
    """
    Reads data from an Excel file and populates an SQLite database with tables based on the data.
    
    Parameters:
    ----------
    file_path : str
        The path to the Excel file (e.g., 'data/input.xlsx') from which data is read.
    
    db_path : str
        The path to the SQLite database file (e.g., 'data/database.db') where the data will be stored.
    
    Debugging:
    ---------
    - Prints messages indicating the progress of loading each sheet and writing it to the database.
    """
    data_dict = read_excel_data(file_path)
    
    with sqlite3.connect(db_path) as conn:
        for sheet, df in data_dict.items():
            create_table_from_df(df, sheet, conn)
            # For debugging purposes.
            print(f"Data from sheet '{sheet}' written to database.")
