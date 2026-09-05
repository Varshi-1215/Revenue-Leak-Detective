import pandas as pd
import numpy as np

np.random.seed(42)

n = 50000

# -----------------------------
# BASIC BUSINESS DATA
# -----------------------------

df = pd.DataFrame({
    "Order_ID": [f"ORD{i:05d}" for i in range(1, n + 1)],
    "Customer_ID": [f"CUST{np.random.randint(1, 10001):05d}" for _ in range(n)],
    "Order_Date": pd.date_range("2025-01-01", periods=n, freq="30min"),
    "Product": np.random.choice(
        ["Laptop", "Smartphone", "Headphones", "TV",
         "Shoes", "Watch", "Furniture", "Kitchen Appliance"],
        n
    ),
    "Category": np.random.choice(
        ["Electronics", "Fashion", "Home", "Accessories"],
        n
    ),
    "Region": np.random.choice(
        ["North", "South", "East", "West"],
        n
    ),
    "Quantity": np.random.randint(1, 5, n),
    "Unit_Price": np.random.randint(500, 50000, n),
    "Payment_Method": np.random.choice(
        ["UPI", "Credit Card", "Debit Card", "Net Banking"],
        n
    ),
    "Marketing_Channel": np.random.choice(
        ["Instagram", "Google", "Email", "Direct", "Referral"],
        n
    )
})

# -----------------------------
# REVENUE & DISCOUNT
# -----------------------------

df["Gross_Amount"] = df["Quantity"] * df["Unit_Price"]

df["Discount"] = np.random.choice(
    [0, 5, 10, 15, 20, 25, 30],
    n,
    p=[0.10, 0.15, 0.20, 0.20, 0.15, 0.12, 0.08]
)

df["Revenue"] = df["Gross_Amount"] * (1 - df["Discount"] / 100)

# -----------------------------
# COST & PROFIT
# -----------------------------

df["Cost"] = df["Revenue"] * np.random.uniform(0.55, 0.85, n)

df["Profit"] = df["Revenue"] - df["Cost"]

# -----------------------------
# PAYMENT LEAK
# -----------------------------

df["Payment_Status"] = np.random.choice(
    ["Success", "Failed"],
    n,
    p=[0.92, 0.08]
)

# Failed payments = lost revenue
df["Lost_Revenue_Payment"] = np.where(
    df["Payment_Status"] == "Failed",
    df["Revenue"],
    0
)

# -----------------------------
# DELIVERY
# -----------------------------

df["Delivery_Days"] = np.random.randint(1, 15, n)

# -----------------------------
# ORDER STATUS
# -----------------------------

df["Order_Status"] = "Completed"

# Long delivery → higher cancellation probability
long_delivery = df["Delivery_Days"] >= 10

cancel_random = np.random.random(n)

df.loc[
    long_delivery & (cancel_random < 0.25),
    "Order_Status"
] = "Cancelled"

# Random returns
return_random = np.random.random(n)

df.loc[
    (df["Order_Status"] == "Completed") & (return_random < 0.08),
    "Order_Status"
] = "Returned"

# -----------------------------
# RETURN REVENUE LOSS
# -----------------------------

df["Lost_Revenue_Return"] = np.where(
    df["Order_Status"] == "Returned",
    df["Revenue"],
    0
)

# -----------------------------
# CUSTOMER BEHAVIOUR
# -----------------------------

df["Last_Purchase_Days"] = np.random.randint(1, 181, n)

df["Customer_Rating"] = np.round(
    np.random.uniform(1, 5, n), 1
)

# Long delivery → lower rating
df.loc[
    df["Delivery_Days"] >= 10,
    "Customer_Rating"
] = np.round(
    np.random.uniform(1.0, 3.2, long_delivery.sum()),
    1
)

# -----------------------------
# CUSTOMER SEGMENT
# -----------------------------

df["Customer_Segment"] = np.where(
    (df["Last_Purchase_Days"] > 90) & (df["Revenue"] > 30000),
    "High Value At Risk",
    np.where(
        df["Last_Purchase_Days"] > 90,
        "At Risk",
        np.where(
            df["Revenue"] > 30000,
            "High Value",
            "Regular"
        )
    )
)

# -----------------------------
# DISCOUNT LEAK
# -----------------------------

df["Discount_Leak"] = np.where(
    (df["Discount"] >= 25) & (df["Profit"] < df["Revenue"] * 0.20),
    df["Revenue"] * 0.10,
    0
)

# -----------------------------
# TOTAL POTENTIAL REVENUE LEAK
# -----------------------------

df["Potential_Revenue_Leak"] = (
    df["Lost_Revenue_Payment"]
    + df["Lost_Revenue_Return"]
    + df["Discount_Leak"]
)

# -----------------------------
# SAVE DATASET
# -----------------------------

df.to_csv(
    "data/revenue_data.csv",
    index=False
)

print("====================================")
print("Revenue Leak Detective Dataset Ready!")
print("====================================")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print()
print("Payment Failures:", (df["Payment_Status"] == "Failed").sum())
print("Cancelled Orders:", (df["Order_Status"] == "Cancelled").sum())
print("Returned Orders:", (df["Order_Status"] == "Returned").sum())
print("High Value At Risk:",
      (df["Customer_Segment"] == "High Value At Risk").sum())
print()
print("Total Revenue:",
      round(df["Revenue"].sum(), 2))
print("Potential Revenue Leak:",
      round(df["Potential_Revenue_Leak"].sum(), 2))
print()
print(df.head())