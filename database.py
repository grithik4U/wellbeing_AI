import sqlite3
import os
import pandas as pd

# Database setup
DB_PATH = "data/responses.db"

def init_db():
    """Initialize the database and create necessary tables if they don't exist"""
    # Make sure data directory exists
    if not os.path.exists("data"):
        try:
            os.makedirs("data")
        except FileExistsError:
            pass

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create responses table with dynamic columns for all questions
    c.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        response_id TEXT PRIMARY KEY,
        timestamp TIMESTAMP,
        department TEXT,
        location TEXT,
        q_1 INTEGER,
        q_2 INTEGER,
        q_3 INTEGER,
        q_4 INTEGER,
        q_5 INTEGER,
        q_6 INTEGER,
        q_7 INTEGER,
        q_8 INTEGER,
        q_9 TEXT,
        q_10 TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def save_response(response_data):
    """Save a survey response to the database"""
    conn = sqlite3.connect(DB_PATH)
    
    # Convert the dictionary to a DataFrame with a single row
    df = pd.DataFrame([response_data])
    
    # Save to SQLite
    df.to_sql('responses', conn, if_exists='append', index=False)
    
    conn.close()

def get_responses():
    """Get all responses from the database"""
    # Check if database exists
    if not os.path.exists(DB_PATH):
        init_db()
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Read all responses
        df = pd.read_sql_query("SELECT * FROM responses", conn, parse_dates=["timestamp"])
        conn.close()
        return df
    except:
        conn.close()
        # If table doesn't exist, initialize DB and return empty DataFrame
        init_db()
        return pd.DataFrame()

def get_filtered_responses(start_date=None, end_date=None, department=None, location=None):
    """Get filtered responses based on criteria"""
    conn = sqlite3.connect(DB_PATH)
    
    query = "SELECT * FROM responses WHERE 1=1"
    params = []
    
    if start_date:
        query += " AND timestamp >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND timestamp <= ?"
        params.append(end_date)
    
    if department and department != "All":
        query += " AND department = ?"
        params.append(department)
    
    if location and location != "All":
        query += " AND location = ?"
        params.append(location)
    
    try:
        df = pd.read_sql_query(query, conn, params=params, parse_dates=["timestamp"])
        conn.close()
        return df
    except:
        conn.close()
        return pd.DataFrame()

# Initialize database on import
init_db()