"""
Create the MySQL database on Railway
"""
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Railway MySQL connection details
db_host = os.getenv("MYSQLHOST", "mysql.railway.internal")
db_user = os.getenv("MYSQLUSER", "root")
db_pass = os.getenv("MYSQLPASSWORD", "")
db_port = int(os.getenv("MYSQLPORT", "3306"))

# Connect to Railway MySQL server
try:
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        port=db_port
    )
    
    cursor = connection.cursor()
    
    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS transaction_classifier")
    print("✅ Database 'transaction_classifier' created successfully!")
    
    # Show all databases to confirm
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("\nAvailable databases:")
    for db in databases:
        print(f"  - {db[0]}")
    
    cursor.close()
    connection.close()
    print("\n✅ Done! Now run: python init_db.py")
    
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
