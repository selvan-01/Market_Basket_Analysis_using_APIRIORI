# ================================
# 📌 Market Basket Analysis using Apriori
# ================================

# ----------- 1. Import Libraries -----------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------- 2. Load Dataset -----------
# If using local file (VS Code / PyCharm)
dataset = pd.read_csv('dataset.csv')

# Display basic info
print("Dataset Shape:", dataset.shape)
print("\nFirst 5 Rows:\n", dataset.head())

# ----------- 3. Data Preprocessing -----------
# Convert dataset into list of transactions
# Each row = one transaction (customer purchase)

transactions = []

# Loop through all rows (transactions)
for i in range(0, dataset.shape[0]):
    
    # Each transaction contains 20 items
    transaction = []
    
    for j in range(0, dataset.shape[1]):
        item = str(dataset.values[i, j])
        
        # Ignore 'nan' values
        if item != 'nan':
            transaction.append(item)
    
    transactions.append(transaction)

print("\nSample Transaction:", transactions[0])

# ----------- 4. Install & Import Apriori -----------
# Run this only once in terminal:
# pip install apyori

from apyori import apriori

# ----------- 5. Apply Apriori Algorithm -----------
rules = apriori(
    transactions=transactions,
    min_support=0.003,     # Minimum frequency of item
    min_confidence=0.2,    # Rule reliability
    min_lift=3,            # Strength of association
    min_length=2,
    max_length=2
)

# Convert rules to list
results = list(rules)

# ----------- 6. Extract Results -----------
lhs = []   # Left side (Item A)
rhs = []   # Right side (Item B)
support = []
confidence = []
lift = []

for result in results:
    for relation in result[2]:
        lhs.append(tuple(relation[0])[0])
        rhs.append(tuple(relation[1])[0])
        support.append(result[1])
        confidence.append(relation[2])
        lift.append(relation[3])

# ----------- 7. Convert to DataFrame -----------
results_df = pd.DataFrame({
    'Left Hand Side': lhs,
    'Right Hand Side': rhs,
    'Support': support,
    'Confidence': confidence,
    'Lift': lift
})

# Sort by Lift (important metric)
results_df = results_df.sort_values(by='Lift', ascending=False)

# ----------- 8. Final Output -----------
print("\nTop Association Rules:\n")
print(results_df.head(10))