import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# 1. Load dataset
df = pd.read_csv("transactions_dataset_500_rich.csv")
print("Original Data:")
print(df.head())

# 2. Separate features and labels
X = df.drop(columns=["txn_id", "label"])
y = df["label"]

# 3. Convert text → numbers
categorical_cols = ["sender_country", "receiver_country", 
                    "payment_method", "merchant_category", "ip_address"]

le = LabelEncoder()
for col in categorical_cols:
    X[col] = le.fit_transform(X[col])

print("\nAfter Label Encoding:")
print(X.head())

# 4. Scale the 'amount' column
scaler = StandardScaler()
X["amount"] = scaler.fit_transform(X[["amount"]])

print("\nAfter Scaling Amount:")
print(X.head())

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nShapes:")
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)
