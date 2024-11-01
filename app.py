from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/reviews', methods=['GET'])
def get_reviews():
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews').fetchall()
    conn.close()
    return jsonify([dict(review) for review in reviews])

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    
    # Tjek om data er en liste (flere anmeldelser) eller en enkelt dict (én anmeldelse)
    if isinstance(data, list):
        reviews = data
    else:
        reviews = [data]  # Pak enkelt objekt i en liste for konsistens
    
    conn = get_db_connection()
    try:
        for review in reviews:
            conn.execute(
                '''
                INSERT INTO reviews (first_name, last_name, email, booking_number, room_type, country, days_rented, review)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    review['first_name'],
                    review['last_name'],
                    review['email'],
                    review['booking_number'],
                    review['room_type'],
                    review['country'],
                    review['days_rented'],
                    review['review']
                )
            )
        conn.commit()
    except sqlite3.IntegrityError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

    return jsonify({"message": "Anmeldelser tilføjet succesfuldt"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)