import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# -------------------------
# Load env
# -------------------------
load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# -------------------------
# Flask + DB setup
# -------------------------
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = SECRET_KEY

# SQLAlchemy connection string (mysql+mysqlconnector)
app.config['SQLALCHEMY_DATABASE_URI'] =  "mysql+mysqlconnector://root:Dkmysql%40123@localhost:3306/transaction_classifier"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# -------------------------
# Models
# -------------------------
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


# -------------------------
# Load local model pipeline
# -------------------------
print("=" * 60)
print("🚀 Transaction Classifier — Local Fine-Tuned Model Mode Starting...")
print("=" * 60)
print(f"📂 Loading fine-tuned model from: {MODEL_PATH}")

try:
    # Load tokenizer and model separately with local_files_only
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
    
    # Create pipeline with pre-loaded components
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load model from {MODEL_PATH}: {e}")
    raise SystemExit(e)

print("=" * 60)

# label_map - ensure matches your fine-tuned model's label tokens
label_map = {
    "LABEL_0": "Legal ✅",
    "LABEL_1": "Illegal ❌",
    "LABEL_2": "Suspicious ⚠️"
}


# -------------------------
# Helper: Reason logic (same as previous)
# -------------------------
def get_reason(text, label):
    text = (text or "").lower()
    if "legal" in label.lower():
        if any(word in text for word in ["salary", "credited", "approved", "completed", "authorized", "payment", "invoice"]):
            return "This transaction appears to be a verified or authorized financial activity."
        return "No illegal or suspicious terms detected, indicating lawful activity."
    if "illegal" in label.lower():
        if any(word in text for word in ["fraud", "scam", "unauthorized", "bribe", "hack", "drugs", "theft", "fake"]):
            return "Contains keywords typically associated with unlawful or fraudulent activity."
        return "The context suggests a violation of legal or policy standards."
    if "suspicious" in label.lower():
        if any(word in text for word in ["unknown", "unusual", "multiple", "attempt", "transfer", "unclear", "risky"]):
            return "Mentions unclear or unusual transactions, indicating potentially suspicious behavior."
        return "The transaction details seem irregular or incomplete, raising suspicion."
    return "Unable to determine a clear reason for this classification."


# -------------------------
# Authentication helpers
# -------------------------
def logged_in_user_id():
    return session.get("user_id")


def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not logged_in_user_id():
            flash("Please login to continue.", "warning")
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper


# -------------------------
# Routes: Auth
# -------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for("signup"))
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return redirect(url_for("signup"))
        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful — you can login now.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password.", "danger")
            return redirect(url_for("login"))
        session["user_id"] = user.id
        session["username"] = user.username
        flash(f"Welcome, {user.username}!", "success")
        next_page = request.args.get("next") or url_for("index")
        return redirect(next_page)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# -------------------------
# Home / Index (main classifier UI)
# -------------------------
@app.route("/")
@login_required
def index():
    return render_template("index.html", username=session.get("username"))


# -------------------------
# Predict route (unchanged behavior)
# -------------------------
@app.route("/predict", methods=["POST"])
@login_required
def predict():
    data = request.json or {}
    description = data.get("description", "").strip()
    if not description:
        return jsonify({"error": "Description is required"}), 400

    # Build context
    context_parts = []
    if data.get("amount"):
        context_parts.append(f"Amount: ${data['amount']}")
    if data.get("sender_country"):
        context_parts.append(f"From: {data['sender_country']}")
    if data.get("receiver_country"):
        context_parts.append(f"To: {data['receiver_country']}")
    if data.get("payment_method"):
        context_parts.append(f"Payment method: {data['payment_method']}")
    if data.get("merchant_category"):
        context_parts.append(f"Category: {data['merchant_category']}")

    input_text = f"{description}. {', '.join(context_parts)}" if context_parts else description

    try:
        result = classifier(input_text)[0]
        raw_label = result["label"]
        score = float(result.get("score", 0.0))
        label = label_map.get(raw_label.upper(), raw_label)
        reason = get_reason(input_text, label)

        return jsonify({
            "label": label,
            "score": score,
            "reason": reason,
            "all_predictions": [result]
        })
    except Exception as e:
        return jsonify({"error": f"Model inference failed: {str(e)}"}), 500


# -------------------------
# Save to history (requires login)
# -------------------------
@app.route("/save", methods=["POST"])
@login_required
def save_transaction():
    data = request.json or {}
    user_id = logged_in_user_id()
    description = data.get("description", "").strip()
    if not description:
        return jsonify({"error": "Description required"}), 400

    # parse optional fields
    amount = data.get("amount")
    try:
        amount_val = float(amount) if amount not in (None, "", []) else None
    except Exception:
        amount_val = None

    tx = Transaction(
        user_id=user_id,
        description=description,
        amount=amount_val,
        sender_country=data.get("sender_country"),
        receiver_country=data.get("receiver_country"),
        payment_method=data.get("payment_method"),
        merchant_category=data.get("merchant_category"),
        predicted_label=data.get("label"),
        confidence=float(data.get("score", 0.0)),
        reason=data.get("reason")
    )
    db.session.add(tx)
    db.session.commit()
    return jsonify({"success": True, "id": tx.id})


# -------------------------
# History page (shows saved transactions for logged-in user)
# -------------------------
@app.route("/history")
@login_required
def history():
    user_id = logged_in_user_id()
    rows = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
    return render_template("history.html", rows=rows)


# -------------------------
# Reports page (aggregated stats)
# -------------------------
@app.route("/reports")
@login_required
def reports():
    user_id = logged_in_user_id()

    # ✅ use .filter instead of .filter_by for LIKE operations
    legal_count = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.predicted_label.like("%Legal%")
    ).count()

    illegal_count = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.predicted_label.like("%Illegal%")
    ).count()

    suspicious_count = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.predicted_label.like("%Suspicious%")
    ).count()

    total = legal_count + illegal_count + suspicious_count

    return render_template(
        "reports.html",
        legal=legal_count,
        illegal=illegal_count,
        suspicious=suspicious_count,
        total=total
    )



# -------------------------
# API endpoint used by reports page for chart data
# -------------------------
@app.route("/api/reports/data")
@login_required
def reports_data():
    user_id = logged_in_user_id()
    legal = Transaction.query.filter_by(user_id=user_id).filter(Transaction.predicted_label.like("%Legal%")).count()
    illegal = Transaction.query.filter_by(user_id=user_id).filter(Transaction.predicted_label.like("%Illegal%")).count()
    suspicious = Transaction.query.filter_by(user_id=user_id).filter(Transaction.predicted_label.like("%Suspicious%")).count()
    return jsonify({"legal": legal, "illegal": illegal, "suspicious": suspicious})


# -------------------------
# Initialize DB (create tables) - run once
# -------------------------
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Initialized the database (tables created).")


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
