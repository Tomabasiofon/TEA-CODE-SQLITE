import sqlite3

def initialize_database():
    """
    This was used to initializes database. Optional function which will be removed"""
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    # Create tables for each sheet
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capex_factors (
            Category TEXT,
            Value REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opex_factors (
            Category TEXT,
            Value REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS electrolyser (
            Category TEXT,
            Value REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cash_flow (
            Category TEXT,
            Value REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pretreat_equipment_cost (
            Category TEXT,
            Value REAL
        )
    ''')

    # Insert sample data or load data from your Excel files
    # ...neww

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()