from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        booking_number TEXT UNIQUE NOT NULL,
        room_type TEXT NOT NULL,
        country TEXT NOT NULL,
        days_rented INTEGER NOT NULL,
        review TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route('/reviews', methods=['GET'])
def get_reviews():
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in reviews])

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    
    # Check if data is a list (multiple reviews) or a single dict (one review)
    if isinstance(data, list):
        reviews = data
    else:
        reviews = [data]  # Wrap single object in a list for consistency
    
    conn = get_db_connection()
    try:
        for review in reviews:
            conn.execute(
                '''INSERT INTO reviews (first_name, last_name, email, booking_number, room_type, country, days_rented, review)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (review['first_name'], review['last_name'], review['email'], review['booking_number'], review['room_type'],
                 review['country'], review['days_rented'], review['review'])
            )
        conn.commit()
    except sqlite3.IntegrityError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

    return jsonify({"message": "reviews added successfully"}), 201

if __name__ == '__main__':
    initialize_database()  # Ensure the table exists on startup
    app.run(debug=True, host='0.0.0.0', port=5000)