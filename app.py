from flask import Flask, jsonify, request, make_response
import sqlite3
from io import StringIO
import csv

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
    
    # Check if data is a list (multiple reviews) or a single dict (one review)
    if isinstance(data, list):
        reviews = data
    else:
        reviews = [data]  # Wrap single object in a list for consistency
    
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

    return jsonify({"message": "Reviews added successfully"}), 201

# Export reviews to CSV
@app.route('/reviews/csv', methods=['GET'])
def export_reviews_csv():
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews').fetchall()
    conn.close()
    
    si = StringIO()
    writer = csv.writer(si)
    
    # Write CSV header
    writer.writerow([
        'Review ID',
        'First Name',
        'Last Name',
        'Email',
        'Booking Number',
        'Room Type',
        'Country',
        'Days Rented',
        'Review'
    ])
    
    # Write review data
    for review in reviews:
        writer.writerow([
            review['id'],  # Assuming there's an 'id' column in your table
            review['first_name'],
            review['last_name'],
            review['email'],
            review['booking_number'],
            review['room_type'],
            review['country'],
            review['days_rented'],
            review['review']
        ])
    
    # Create a response with the CSV data
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=reviews.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)