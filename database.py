import sqlite3
from sqlite3 import Error

def create_connection():
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect('cinetech.db')
        return conn
    except Error as e:
        print(e)
    
    return conn

def initialize_database():
    """Initialize the database with required tables"""
    conn = create_connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Create students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    grades TEXT NOT NULL
                )
            ''')
            
            # Create employees table (pre-populated with 10 employees as requested)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    salary REAL NOT NULL,
                    age INTEGER NOT NULL,
                    position TEXT NOT NULL
                )
            ''')
            
            # Check if employees table is empty and insert sample data
            cursor.execute("SELECT COUNT(*) FROM employees")
            count = cursor.fetchone()[0]
            
            if count == 0:
                employees = [
                            ("Shivam Kumar", "Plot No. 12, MG Road, Mumbai, India", 60000, 34, "Manager"),
                            ("Junaid Ali", "Banjara Hills, Hyderabad, India", 55000, 32, "Assistant Manager"),
                            ("Aharnish Dhaw Kumar", "Sector 18, Noida, Uttar Pradesh, India", 52000, 36, "Project Lead"),
                            ("Daya Shankar", "BTM Layout, Bengaluru, Karnataka, India", 48000, 29, "Senior Developer"),
                            ("Amar Kumar", "Ashok Nagar, Patna, Bihar, India", 45000, 32, "Developer"),
                            ("Shahnawaz Akthar", "Rajbagh, Srinagar, J&K, India", 40000, 28, "Junior Developer"),
                            ("Prem Kumar Yadav", "Harmu Colony, Ranchi, Jharkhand, India", 38000, 30, "Designer"),
                            ("Sameer Ahmad", "Park Street, Kolkata, West Bengal, India", 37000, 27, "Marketing Specialist"),
                            ("Rahul Kumar", "Gomti Nagar, Lucknow, Uttar Pradesh, India", 35000, 26, "Sales Associate"),
                            ("Sumit Kumar", "Sector 22, Chandigarh, India", 32000, 25, "Customer Support")
                                    ]
                
                cursor.executemany('''
                    INSERT INTO employees (name, address, salary, age, position)
                    VALUES (?, ?, ?, ?, ?)
                ''', employees)
            
            # Create finance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS finance (
                    id INTEGER PRIMARY KEY,
                    pin INTEGER NOT NULL,
                    balance REAL NOT NULL
                )
            ''')
            
            # Insert default finance data if not exists
            cursor.execute("SELECT COUNT(*) FROM finance")
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute('''
                    INSERT INTO finance (id, pin, balance)
                    VALUES (1, 1234, 10000)
                ''')
            
            conn.commit()
            
        except Error as e:
            print(e)
        finally:
            conn.close()

# Initialize the database when this module is imported
initialize_database()
# This module initializes the database and creates necessary tables.
# It also pre-populates the employees table with 10 sample employees.
# The finance table is initialized with a default balance and pin.      