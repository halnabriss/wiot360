from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)

# MySQL configuration (using environment variables for security)
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'my-secret-pw')
MYSQL_DB = os.getenv('MYSQL_DB', 'ip_addresses')

# Establish MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

@app.route('/')
def capture_ip():
    ip_address = request.remote_addr
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO ip_addresses (ip) VALUES (%s)", (ip_address,))
    connection.commit()
    cursor.close()
    connection.close()
    return f"Captured IP address: {ip_address}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
