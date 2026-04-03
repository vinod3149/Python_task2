import sqlite3

def initialize_database():
    conn = sqlite3.connect('bmi_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_record(name, weight, height, bmi, category):
    """Saves a single BMI record to the database."""
    conn = sqlite3.connect('bmi_history.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (name, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
                   (name, weight, height, bmi, category))
    conn.commit()
    conn.close()

def load_records(name):
    """Loads records for a specific user for trend analysis."""
    conn = sqlite3.connect('bmi_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, bmi FROM records WHERE name = ? ORDER BY timestamp ASC", (name,))
    records = cursor.fetchall()
    conn.close()
    return records

def load_all_records():
    """Loads all records from the database for the history view."""
    conn = sqlite3.connect('bmi_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, name, bmi, category FROM records ORDER BY timestamp DESC")
    records = cursor.fetchall()
    conn.close()
    return records
