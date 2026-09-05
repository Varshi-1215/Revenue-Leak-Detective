import pandas as pd

# Load dataset
df = pd.read_csv("data/revenue_data.csv")

print("====================================")
print("REVENUE LEAK ANALYSIS")
print("====================================")

# Basic metrics
print("\nTotal Revenue:", round(df["Revenue"].sum(), 2))
print("Total Profit:", round(df["Profit"].sum(), 2))
print("Potential Revenue Leak:", round(df["Potential_Revenue_Leak"].sum(), 2))

# Leak sources
print("\n--- LEAK SOURCES ---")

print("Payment Failure Loss:",
      round(df["Lost_Revenue_Payment"].sum(), 2))

print("Return Revenue Loss:",
      round(df["Lost_Revenue_Return"].sum(), 2))

print("Discount Leak:",
      round(df["Discount_Leak"].sum(), 2))

# Orders
print("\n--- ORDER PROBLEMS ---")

print("Payment Failures:",
      (df["Payment_Status"] == "Failed").sum())

print("Cancelled Orders:",
      (df["Order_Status"] == "Cancelled").sum())

print("Returned Orders:",
      (df["Order_Status"] == "Returned").sum())

# Customers
print("\n--- CUSTOMER RISK ---")

print("High Value At Risk Customers:",
      (df["Customer_Segment"] == "High Value At Risk").sum())

print("\n====================================")
print("Analysis Complete!")
print("====================================")
print("\n--- PRODUCT ANALYSIS ---")

product_analysis = df.groupby("Product").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Revenue_Leak=("Potential_Revenue_Leak", "sum")
).sort_values("Revenue_Leak", ascending=False)

print(product_analysis)
print("\n--- REGION ANALYSIS ---")

region_analysis = df.groupby("Region").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Revenue_Leak=("Potential_Revenue_Leak", "sum")
).sort_values("Revenue_Leak", ascending=False)

print(region_analysis)
print("\n--- CUSTOMER SEGMENT ANALYSIS ---")

customer_analysis = df.groupby("Customer_Segment").agg(
    Customers=("Customer_ID", "nunique"),
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum")
).sort_values("Revenue", ascending=False)

print(customer_analysis)
print("\n--- TOP CUSTOMER RECOVERY OPPORTUNITIES ---")

top_customers = df[
    df["Customer_Segment"] == "High Value At Risk"
].groupby("Customer_ID").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Last_Purchase_Days=("Last_Purchase_Days", "max"),
    Customer_Rating=("Customer_Rating", "mean")
).sort_values("Revenue", ascending=False).head(10)

print(top_customers)
# Save summary for Power BI
summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Profit",
        "Potential Revenue Leak",
        "Payment Failure Loss",
        "Return Revenue Loss",
        "Discount Leak",
        "Payment Failures",
        "Cancelled Orders",
        "Returned Orders",
        "High Value At Risk Customers"
    ],
    "Value": [
        df["Revenue"].sum(),
        df["Profit"].sum(),
        df["Potential_Revenue_Leak"].sum(),
        df["Lost_Revenue_Payment"].sum(),
        df["Lost_Revenue_Return"].sum(),
        df["Discount_Leak"].sum(),
        (df["Payment_Status"] == "Failed").sum(),
        (df["Order_Status"] == "Cancelled").sum(),
        (df["Order_Status"] == "Returned").sum(),
        df[df["Customer_Segment"] == "High Value At Risk"]["Customer_ID"].nunique()
    ]
})

summary.to_csv("data/powerbi_summary.csv", index=False)

print("\nPower BI summary created successfully!")