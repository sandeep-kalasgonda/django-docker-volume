from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'mysql',
    'user': 'phoenix_project',
    'password': 'ph8Enixx@482344',
    'database': 'my_database'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return "Welcome to the Flask application!"

@app.route('/create-table', methods=['POST'])
def create_table():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Table created successfully!'})
    return jsonify({'message': 'Failed to connect to the database!'})

@app.route('/add-user', methods=['POST'])
def add_user():
    user_data = request.json
    name = user_data.get('name')
    email = user_data.get('email')

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'User added successfully!'})
    return jsonify({'message': 'Failed to connect to the database!'})

@app.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(users)
    return jsonify({'message': 'Failed to connect to the database!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

