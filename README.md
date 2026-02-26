# 🔐 Transaction Classifier Web Application

A Flask-based web application that uses AI to classify financial transactions as **Legal ✅**, **Suspicious ⚠️**, or **Illegal ❌** using a fine-tuned DistilBERT model.

## 🚀 Features

- **🤖 AI-Powered Classification**: Local fine-tuned DistilBERT model for accurate transaction analysis
- **👤 User Authentication**: Secure login/signup system with password hashing
- **💾 Database Integration**: MySQL database for storing users and transaction history
- **📊 Transaction History**: View all your classified transactions with details
- **📈 Analytics Dashboard**: Visual reports with charts showing classification statistics
- **🎨 Modern UI**: Clean, responsive design with dark theme
- **🔒 Protected Routes**: Login required for accessing main features
- **💡 Smart Reasoning**: AI-generated explanations for each classification

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.x)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Model**: Fine-tuned DistilBERT (local inference)
- **Database**: MySQL with SQLAlchemy ORM
- **Security**: Werkzeug password hashing, Flask sessions
- **ML Framework**: Hugging Face Transformers

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server (running on localhost:3306)
- Git (optional)

## ⚙️ Installation & Setup

### 1. Install Dependencies

```bash
cd web_pages
pip install -r requirements.txt
```

**Required packages:**
- Flask
- Flask-SQLAlchemy
- mysql-connector-python
- transformers
- torch
- python-dotenv
- werkzeug

### 2. Configure MySQL Database

Make sure MySQL is running with the following credentials (or update in `app.py`):
- **Host**: localhost
- **Port**: 3306
- **User**: root
- **Password**: ______

### 3. Create Database and Tables

Run the setup scripts in order:

```bash
# Create the database
python create_database.py

# Create tables (users, transactions)
python init_db.py
```

### 4. Verify Model Files

Ensure the fine-tuned model is present in:
```
web_pages/fine_tuned_distilbert/
├── config.json
├── model.safetensors
├── tokenizer.json
├── tokenizer_config.json
├── special_tokens_map.json
└── vocab.txt
```

### 5. Run the Application

```bash
python app.py
```

The application will start on: **http://localhost:5000**

## 📖 Usage Guide

### First Time Setup

1. **Navigate to** `http://localhost:5000`
2. You'll be redirected to the **login page**
3. Click **"Sign Up"** to create a new account
4. Enter username and password
5. After successful signup, **login** with your credentials

### Classifying Transactions

1. After login, you'll see the main classification interface
2. Fill in the transaction details:
   - **Description** (required): Brief description of the transaction
   - **Amount** (optional): Transaction amount in USD
   - **Sender Country** (optional): Country of origin
   - **Receiver Country** (optional): Destination country
   - **Payment Method** (optional): e.g., credit_card, crypto, bank_transfer
   - **Merchant Category** (optional): e.g., retail, gambling, entertainment

3. Click **"Classify Transaction"**
4. View results:
   - Classification label (Legal/Illegal/Suspicious)
   - Confidence score (0-1)
   - AI-generated reasoning

5. **Save to History** to store the result in your account

### Viewing History

- Navigate to **"History"** from the menu
- View all your saved transactions
- See details: date, description, classification, confidence, and reasoning

### Analytics Reports

- Navigate to **"Reports"** from the menu
- View statistics:
  - Total transactions
  - Legal count
  - Illegal count
  - Suspicious count
- Interactive pie chart visualization

## 🗂️ Project Structure

```
web_pages/
├── app.py                      # Main Flask application
├── create_database.py          # Database creation script
├── init_db.py                  # Table initialization script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── fine_tuned_distilbert/      # AI model files
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer.json
│   └── ...
├── templates/                  # HTML templates
│   ├── base_history.html       # Base template
│   ├── index.html              # Main classifier page
│   ├── login.html              # Login page
│   ├── signup.html             # Signup page
│   ├── history.html            # Transaction history
│   └── reports.html            # Analytics dashboard
└── static/                     # CSS and JavaScript
    ├── style.css               # Global styles
    └── script.js               # Client-side logic
```

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in `web_pages/` directory:

```env
SECRET_KEY=your_secret_key_here
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=*****
DB_NAME=transaction_classifier
MODEL_PATH=./fine_tuned_distilbert
PORT=5000
```

### Database Configuration

Update in `app.py` if using different credentials:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://user:password@host:port/database"
```

## 🐛 Troubleshooting

### Database Connection Error

**Error**: `Unknown database 'transaction_classifier'`

**Solution**: Run `python create_database.py` first

---

**Error**: `Unknown column 'users.password_hash'`

**Solution**: Run `python init_db.py` to create tables

---

### Model Loading Issues

**Error**: Model files not found

**Solution**: Ensure `fine_tuned_distilbert/` directory exists with all model files

---

### Port Already in Use

**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)  # Change 5000 to 5001
```

---

### Permission Denied (MySQL)

**Solution**: Check MySQL user permissions:
```sql
GRANT ALL PRIVILEGES ON transaction_classifier.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## 🔐 Security Notes

- Passwords are hashed using Werkzeug's `generate_password_hash()`
- Sessions are secured with Flask's secret key
- Login required for all main features
- SQL injection protection via SQLAlchemy ORM
- Never commit `.env` files with credentials

## 📊 Model Information

- **Architecture**: DistilBERT (distilled BERT)
- **Training**: Fine-tuned on financial transaction data
- **Labels**:
  - `LABEL_0`: Legal ✅
  - `LABEL_1`: Illegal ❌
  - `LABEL_2`: Suspicious ⚠️
- **Inference**: Local (no external API calls)

## 🤝 Contributing

Feel free to submit issues or pull requests for improvements!

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Developed by Dineshkumar

---

**⭐ If you find this project useful, please give it a star!**

