from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = PROJECT_ROOT / "data" / "raw"


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING DATA")
print("=" * 70)

dim_customer = pd.read_csv(
    DATA_RAW / "dim_customer.csv"
)

dim_date = pd.read_csv(
    DATA_RAW / "dim_date.csv",
    parse_dates=["date"]
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

print("Customer rows:", len(dim_customer))
print("Date rows:", len(dim_date))
print("Product rows:", len(dim_product))
print("Region rows:", len(dim_region))
print("Sales rows:", len(fact_sales))


# ============================================================
# 3. BASIC STRUCTURE
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC STRUCTURE")
print("=" * 70)

print("\nCustomer columns:")
print(dim_customer.columns.tolist())

print("\nDate columns:")
print(dim_date.columns.tolist())

print("\nProduct columns:")
print(dim_product.columns.tolist())

print("\nRegion columns:")
print(dim_region.columns.tolist())

print("\nFact Sales columns:")
print(fact_sales.columns.tolist())


# ============================================================
# 4. NULL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("2. NULL VALIDATION")
print("=" * 70)

datasets = {
    "Dim Customer": dim_customer,
    "Dim Date": dim_date,
    "Dim Product": dim_product,
    "Dim Region": dim_region,
    "Fact Sales": fact_sales,
}

for name, df in datasets.items():

    total_nulls = df.isna().sum().sum()

    print(
        f"{name}: {total_nulls} missing values"
    )

    if total_nulls > 0:
        print(df.isna().sum())


# ============================================================
# 5. DUPLICATE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("3. DUPLICATE VALIDATION")
print("=" * 70)

print(
    "Duplicate customer IDs:",
    dim_customer["customer_id"].duplicated().sum()
)

print(
    "Duplicate product IDs:",
    dim_product["product_id"].duplicated().sum()
)

print(
    "Duplicate region IDs:",
    dim_region["region_id"].duplicated().sum()
)

print(
    "Duplicate dates:",
    dim_date["date"].duplicated().sum()
)

print(
    "Duplicate sales IDs:",
    fact_sales["sales_id"].duplicated().sum()
)


# ============================================================
# 6. FOREIGN KEY VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("4. FOREIGN KEY VALIDATION")
print("=" * 70)

customer_ids = set(
    dim_customer["customer_id"]
)

product_ids = set(
    dim_product["product_id"]
)

region_ids = set(
    dim_region["region_id"]
)

invalid_customers = (
    ~fact_sales["customer_id"].isin(customer_ids)
).sum()

invalid_products = (
    ~fact_sales["product_id"].isin(product_ids)
).sum()

invalid_regions = (
    ~fact_sales["region_id"].isin(region_ids)
).sum()

print(
    "Invalid customer IDs:",
    invalid_customers
)

print(
    "Invalid product IDs:",
    invalid_products
)

print(
    "Invalid region IDs:",
    invalid_regions
)


# ============================================================
# 7. DATE RANGE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("5. DATE RANGE VALIDATION")
print("=" * 70)

date_min = dim_date["date"].min()
date_max = dim_date["date"].max()

sales_min = fact_sales["order_date"].min()
sales_max = fact_sales["order_date"].max()

print("Dim Date minimum:", date_min)
print("Dim Date maximum:", date_max)

print("Fact Sales minimum:", sales_min)
print("Fact Sales maximum:", sales_max)

print(
    "Sales before Date dimension:",
    (fact_sales["order_date"] < date_min).sum()
)

print(
    "Sales after Date dimension:",
    (fact_sales["order_date"] > date_max).sum()
)


# ============================================================
# 8. CUSTOMER SIGNUP DATE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("6. CUSTOMER SIGNUP DATE VALIDATION")
print("=" * 70)

customer_signup = dim_customer[
    ["customer_id", "signup_date"]
].copy()

customer_signup["signup_date"] = pd.to_datetime(
    customer_signup["signup_date"]
)

fact_with_signup = fact_sales.merge(
    customer_signup,
    on="customer_id",
    how="left"
)

sales_before_signup = (
    fact_with_signup["order_date"]
    < fact_with_signup["signup_date"]
).sum()

print(
    "Sales before customer signup:",
    sales_before_signup
)


# ============================================================
# 9. NUMERIC BUSINESS VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("7. NUMERIC BUSINESS VALIDATION")
print("=" * 70)

print(
    "Quantity <= 0:",
    (fact_sales["quantity"] <= 0).sum()
)

print(
    "Unit price <= 0:",
    (fact_sales["unit_price"] <= 0).sum()
)

print(
    "Revenue < 0:",
    (fact_sales["revenue"] < 0).sum()
)

print(
    "Cost < 0:",
    (fact_sales["cost"] < 0).sum()
)


# ============================================================
# 10. REVENUE CALCULATION VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("8. REVENUE CALCULATION VALIDATION")
print("=" * 70)

calculated_revenue = (
    fact_sales["quantity"]
    * fact_sales["unit_price"]
    * (1 - fact_sales["discount_pct"] / 100)
)

revenue_difference = (
    fact_sales["revenue"]
    - calculated_revenue
).abs()

print(
    "Revenue calculation errors:",
    (revenue_difference > 0.01).sum()
)

print(
    "Maximum revenue difference:",
    revenue_difference.max()
)


# ============================================================
# 11. PROFIT CALCULATION VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("9. PROFIT CALCULATION VALIDATION")
print("=" * 70)

calculated_profit = (
    fact_sales["revenue"]
    - fact_sales["cost"]
)

profit_difference = (
    fact_sales["profit"]
    - calculated_profit
).abs()

print(
    "Profit calculation errors:",
    (profit_difference > 0.01).sum()
)

print(
    "Maximum profit difference:",
    profit_difference.max()
)


# ============================================================
# 12. DISCOUNT VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("10. DISCOUNT VALIDATION")
print("=" * 70)

print(
    "Discount below 0:",
    (fact_sales["discount_pct"] < 0).sum()
)

print(
    "Discount above 20:",
    (fact_sales["discount_pct"] > 20).sum()
)

print(
    "Non-promotion rows with discount:",
    (
        (fact_sales["promotion_flag"] == 0)
        &
        (fact_sales["discount_pct"] > 0)
    ).sum()
)

print(
    "Promotion rows with zero discount:",
    (
        (fact_sales["promotion_flag"] == 1)
        &
        (fact_sales["discount_pct"] == 0)
    ).sum()
)


# ============================================================
# 13. CATEGORY / PRODUCT COVERAGE
# ============================================================

print("\n" + "=" * 70)
print("11. PRODUCT COVERAGE")
print("=" * 70)

product_sales = (
    fact_sales["product_id"]
    .nunique()
)

print(
    "Products in Product Dimension:",
    dim_product["product_id"].nunique()
)

print(
    "Products appearing in Sales:",
    product_sales
)

print("\nSales lines by category:")

category_sales = (
    fact_sales
    .merge(
        dim_product[
            ["product_id", "category"]
        ],
        on="product_id",
        how="left"
    )
    .groupby("category")
    .size()
    .sort_values(ascending=False)
)

print(category_sales)


# ============================================================
# 14. REGION COVERAGE
# ============================================================

print("\n" + "=" * 70)
print("12. REGION COVERAGE")
print("=" * 70)

region_sales = (
    fact_sales
    .groupby("region_id")
    .agg(
        sales_lines=("sales_id", "count"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

print(region_sales)


# ============================================================
# 15. CUSTOMER BEHAVIOR
# ============================================================

print("\n" + "=" * 70)
print("13. CUSTOMER BEHAVIOR")
print("=" * 70)

customer_behavior = (
    dim_customer[
        "behavior_profile"
    ]
    .value_counts()
)

print(customer_behavior)


# ============================================================
# 16. SALES BY YEAR
# ============================================================

print("\n" + "=" * 70)
print("14. SALES BY YEAR")
print("=" * 70)

sales_by_year = (
    fact_sales
    .assign(
        year=fact_sales["order_date"].dt.year
    )
    .groupby("year")
    .agg(
        sales_lines=("sales_id", "count"),
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
)

print(sales_by_year)


# ============================================================
# 17. SALES BY MONTH
# ============================================================

print("\n" + "=" * 70)
print("15. SALES BY MONTH")
print("=" * 70)

monthly_sales = (
    fact_sales
    .assign(
        month=fact_sales["order_date"].dt.to_period("M")
    )
    .groupby("month")
    .agg(
        sales_lines=("sales_id", "count"),
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
)

print(monthly_sales)


# ============================================================
# 18. NEGATIVE PROFIT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("16. NEGATIVE PROFIT ANALYSIS")
print("=" * 70)

negative_profit = fact_sales[
    fact_sales["profit"] < 0
].copy()

print(
    "Negative-profit transactions:",
    len(negative_profit)
)

print(
    "Negative-profit revenue:",
    round(
        negative_profit["revenue"].sum(),
        2
    )
)

print(
    "Negative-profit amount:",
    round(
        negative_profit["profit"].sum(),
        2
    )
)

print(
    "Average discount:",
    round(
        negative_profit["discount_pct"].mean(),
        2
    )
)


# ============================================================
# 19. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY VALIDATION COMPLETE")
print("=" * 70)

print("All validation sections executed successfully.")

