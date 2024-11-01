import sqlite3

def initialize_database():
    conn = sqlite3.connect('database.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        booking_number TEXT UNIQUE NOT NULL,
        room_type TEXT NOT NULL,
        country TEXT NOT NULL,
        days_rented INTEGER NOT NULL,
        review TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
    print("Database and table created successfully!")