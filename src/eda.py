from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_OUTPUTS = PROJECT_ROOT / "data" / "outputs"

DATA_OUTPUTS.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING DATA FOR EDA")
print("=" * 70)

dim_customer = pd.read_csv(
    DATA_RAW / "dim_customer.csv"
)

dim_product = pd.read_csv(
    DATA_RAW / "dim_product.csv"
)

dim_region = pd.read_csv(
    DATA_RAW / "dim_region.csv"
)

fact_sales = pd.read_csv(
    DATA_RAW / "fact_sales.csv",
    parse_dates=["order_date"]
)


# ============================================================
# 3. MERGED ANALYTICAL DATASET
# ============================================================

sales = (
    fact_sales
    .merge(
        dim_customer[
            [
                "customer_id",
                "gender",
                "age",
                "city",
                "customer_type",
                "behavior_profile",
            ]
        ],
        on="customer_id",
        how="left",
    )
    .merge(
        dim_product[
            [
                "product_id",
                "product_name",
                "category",
                "subcategory",
                "brand",
                "popularity",
            ]
        ],
        on="product_id",
        how="left",
    )
    .merge(
        dim_region[
            [
                "region_id",
                "region_name",
                "division",
            ]
        ],
        on="region_id",
        how="left",
    )
)


# ============================================================
# 4. DATE ATTRIBUTES
# ============================================================

sales["year"] = sales["order_date"].dt.year

sales["month"] = (
    sales["order_date"]
    .dt.to_period("M")
    .astype(str)
)

sales["month_number"] = (
    sales["order_date"]
    .dt.month
)


# ============================================================
# 5. EDA SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EDA SUMMARY")
print("=" * 70)

print(
    "\nTotal Revenue:",
    round(sales["revenue"].sum(), 2)
)

print(
    "Total Cost:",
    round(sales["cost"].sum(), 2)
)

print(
    "Total Profit:",
    round(sales["profit"].sum(), 2)
)

print(
    "Overall Profit Margin:",
    round(
        sales["profit"].sum()
        / sales["revenue"].sum()
        * 100,
        2
    ),
    "%"
)


# ============================================================
# 6. MONTHLY REVENUE
# ============================================================

monthly_revenue = (
    sales
    .groupby("month")
    ["revenue"]
    .sum()
)

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Revenue")

plt.xlabel("Month")

plt.ylabel("Revenue")

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "monthly_revenue.png",
    dpi=150
)

plt.close()


# ============================================================
# 7. MONTHLY ORDERS
# ============================================================

monthly_orders = (
    sales
    .groupby("month")
    ["order_id"]
    .nunique()
)

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_orders.index,
    monthly_orders.values,
    marker="o"
)

plt.title("Monthly Orders")

plt.xlabel("Month")

plt.ylabel("Orders")

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "monthly_orders.png",
    dpi=150
)

plt.close()


# ============================================================
# 8. REVENUE BY CATEGORY
# ============================================================

category_revenue = (
    sales
    .groupby("category")
    ["revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=category_revenue.values,
    y=category_revenue.index
)

plt.title("Revenue by Category")

plt.xlabel("Revenue")

plt.ylabel("Category")

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "revenue_by_category.png",
    dpi=150
)

plt.close()


# ============================================================
# 9. REVENUE BY REGION
# ============================================================

region_revenue = (
    sales
    .groupby("region_name")
    ["revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=region_revenue.values,
    y=region_revenue.index
)

plt.title("Revenue by Region")

plt.xlabel("Revenue")

plt.ylabel("Region")

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "revenue_by_region.png",
    dpi=150
)

plt.close()


# ============================================================
# 10. CUSTOMER BEHAVIOR
# ============================================================

behavior_counts = (
    dim_customer[
        "behavior_profile"
    ]
    .value_counts()
)

plt.figure(figsize=(8, 6))

sns.barplot(
    x=behavior_counts.index,
    y=behavior_counts.values
)

plt.title("Customer Behavior Profile")

plt.xlabel("Behavior")

plt.ylabel("Customers")

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "customer_behavior.png",
    dpi=150
)

plt.close()


# ============================================================
# 11. PRODUCT POPULARITY
# ============================================================

popularity_counts = (
    dim_product[
        "popularity"
    ]
    .value_counts()
)

plt.figure(figsize=(8, 6))

sns.barplot(
    x=popularity_counts.index,
    y=popularity_counts.values
)

plt.title("Product Popularity")

plt.xlabel("Popularity")

plt.ylabel("Products")

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "product_popularity.png",
    dpi=150
)

plt.close()


# ============================================================
# 12. PROFIT DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    sales["profit"],
    bins=50,
    kde=True
)

plt.title("Profit Distribution")

plt.xlabel("Profit")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "profit_distribution.png",
    dpi=150
)

plt.close()


# ============================================================
# 13. NEGATIVE PROFIT
# ============================================================

negative_profit = sales[
    sales["profit"] < 0
]

plt.figure(figsize=(10, 6))

sns.histplot(
    negative_profit["profit"],
    bins=30
)

plt.title(
    "Negative Profit Transactions"
)

plt.xlabel("Profit")

plt.ylabel("Transactions")

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "negative_profit.png",
    dpi=150
)

plt.close()


# ============================================================
# 14. SALES CHANNEL
# ============================================================

channel_counts = (
    sales[
        "sales_channel"
    ]
    .value_counts()
)

plt.figure(figsize=(8, 6))

sns.barplot(
    x=channel_counts.index,
    y=channel_counts.values
)

plt.title("Sales by Channel")

plt.xlabel("Channel")

plt.ylabel("Sales Lines")

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "sales_channel.png",
    dpi=150
)

plt.close()


# ============================================================
# 15. PAYMENT METHOD
# ============================================================

payment_counts = (
    sales[
        "payment_method"
    ]
    .value_counts()
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=payment_counts.index,
    y=payment_counts.values
)

plt.title("Payment Method Distribution")

plt.xlabel("Payment Method")

plt.ylabel("Sales Lines")

plt.xticks(
    rotation=20
)

plt.tight_layout()

plt.savefig(
    DATA_OUTPUTS / "payment_method.png",
    dpi=150
)

plt.close()


# ============================================================
# 16. SAVE SUMMARY TABLES
# ============================================================

monthly_summary = (
    sales
    .groupby("month")
    .agg(
        sales_lines=("sales_id", "count"),
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum"),
    )
    .reset_index()
)

monthly_summary.to_csv(
    DATA_OUTPUTS / "monthly_summary.csv",
    index=False
)


# ============================================================
# 17. FINISH
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)

print(
    "Charts saved to:",
    DATA_OUTPUTS
)

print(
    "\nFiles created:"
)

for file in sorted(
    DATA_OUTPUTS.iterdir()
):

    print(
        " -",
        file.name
    )

    