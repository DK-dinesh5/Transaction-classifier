"""
Simple script to initialize the database tables without loading the ML model
"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Load environment variables
load_dotenv()

# Flask + DB setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Use Railway MySQL environment variables
db_url = os.getenv("MYSQL_PUBLIC_URL", "")
if not db_url:
    # Fallback: construct from individual env vars
    db_host = os.getenv("MYSQLHOST", "mysql.railway.internal")
    db_user = os.getenv("MYSQLUSER", "root")
    db_pass = os.getenv("MYSQLPASSWORD", "")
    db_port = os.getenv("MYSQLPORT", "3306")
    db_name = os.getenv("MYSQLDATABASE", "railway")
    db_url = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=True)
    sender_country = db.Column(db.String(100), nullable=True)
    receiver_country = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(100), nullable=True)
    merchant_category = db.Column(db.String(150), nullable=True)
    predicted_label = db.Column(db.String(64), nullable=False)
    confidence = db.Column(db.Float, nullable=True)
    reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="transactions")


if __name__ == "__main__":
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - transactions")
