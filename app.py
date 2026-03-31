# =========================================
# 📌 Market Basket Analysis Web App
# =========================================

import streamlit as st
import pandas as pd
from apyori import apriori

# ----------- Page Config -----------
st.set_page_config(
    page_title="Market Basket Analysis",
    page_icon="🛒",
    layout="wide"
)

# ----------- Custom CSS (UI Design) -----------
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #ff6f00;
        }
        .subtext {
            font-size: 18px;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

# ----------- Title Section -----------
st.markdown('<p class="title">🛒 Market Basket Analysis using Apriori</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Discover products that are frequently bought together</p>', unsafe_allow_html=True)

# ----------- File Upload -----------
st.sidebar.header("📂 Upload Dataset")
file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

# ----------- Parameters -----------
st.sidebar.header("⚙️ Set Parameters")
min_support = st.sidebar.slider("Min Support", 0.001, 0.1, 0.003)
min_confidence = st.sidebar.slider("Min Confidence", 0.1, 1.0, 0.2)
min_lift = st.sidebar.slider("Min Lift", 1.0, 10.0, 3.0)

# ----------- Main Logic -----------
if file is not None:
    dataset = pd.read_csv(file)

    st.subheader("📊 Dataset Preview")
    st.dataframe(dataset.head())

    # ----------- Preprocessing -----------
    transactions = []
    for i in range(0, dataset.shape[0]):
        transaction = []
        for j in range(0, dataset.shape[1]):
            item = str(dataset.values[i, j])
            if item != 'nan':
                transaction.append(item)
        transactions.append(transaction)

    st.success("✅ Data Preprocessing Completed")

    # ----------- Run Apriori -----------
    if st.button("🚀 Run Apriori Algorithm"):

        rules = apriori(
            transactions=transactions,
            min_support=min_support,
            min_confidence=min_confidence,
            min_lift=min_lift,
            min_length=2,
            max_length=2
        )

        results = list(rules)

        # ----------- Extract Results -----------
        lhs, rhs, support, confidence, lift = [], [], [], [], []

        for result in results:
            for relation in result[2]:
                lhs.append(tuple(relation[0])[0])
                rhs.append(tuple(relation[1])[0])
                support.append(result[1])
                confidence.append(relation[2])
                lift.append(relation[3])

        results_df = pd.DataFrame({
            'Product A': lhs,
            'Product B': rhs,
            'Support': support,
            'Confidence': confidence,
            'Lift': lift
        })

        results_df = results_df.sort_values(by='Lift', ascending=False)

        # ----------- Display Results -----------
        st.subheader("📈 Association Rules")
        st.dataframe(results_df.head(20))

        # ----------- Highlight Top Rule -----------
        if not results_df.empty:
            top = results_df.iloc[0]
            st.success(f"🔥 Best Rule: {top['Product A']} ➝ {top['Product B']} (Lift: {round(top['Lift'],2)})")

else:
    st.info("👈 Please upload a dataset to start analysis")