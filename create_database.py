"""
Create the MySQL database
"""
import mysql.connector

# Connect to MySQL server (without specifying a database)
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dkmysql@123",
        port=3306
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
