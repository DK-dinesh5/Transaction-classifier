import pandas as pd

# Example dummy dataset
data = {
    "transaction_id": [1, 2, 3],
    "amount": [500, 20000, 75000],
    "sender": ["Alice", "Bob", "Charlie"],
    "receiver": ["X Corp", "Y Inc", "Z Ltd"],
    "receiver_country": ["US", "IR", "XY"],
    "payment_method": ["credit_card", "crypto", "bank_transfer"],
    "merchant_category": ["retail", "gambling", "pharma"],
    "ip_address": ["192.168.1.1", "10.0.0.23", "172.16.0.5"],
    "label": ["Legal", "Suspicious", "Illegal"]
}

df = pd.DataFrame(data)

# Save in the current folder
df.to_csv("transactions_dataset_500_rich.csv", index=False)

print("✅ File created: transactions_dataset_500_rich.csv")
