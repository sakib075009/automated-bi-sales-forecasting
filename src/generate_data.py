# ============================================================
# SYNTHETIC BUSINESS DATA GENERATOR
# Project: Automated Business Intelligence & Sales Forecasting
# ============================================================

from pathlib import Path
import numpy as np
import pandas as pd


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

# Reproducibility
RANDOM_SEED = 42

# Dataset sizes
N_CUSTOMERS = 1_500
N_PRODUCTS = 75
N_REGIONS = 8

# Historical period
START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

# Target number of sales lines
N_SALES = 120_000


# ============================================================
# 2. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_OUTPUTS = PROJECT_ROOT / "data" / "outputs"


# ============================================================
# 3. CREATE REQUIRED DIRECTORIES
# ============================================================

DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
DATA_OUTPUTS.mkdir(parents=True, exist_ok=True)


# ============================================================
# 4. RANDOM NUMBER GENERATOR
# ============================================================

rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# 5. BASIC CONFIGURATION TEST
# ============================================================

print("=" * 60)
print("SYNTHETIC BUSINESS DATA GENERATOR")
print("=" * 60)

print(f"Project root : {PROJECT_ROOT}")
print(f"Customers    : {N_CUSTOMERS:,}")
print(f"Products     : {N_PRODUCTS:,}")
print(f"Regions      : {N_REGIONS:,}")
print(f"Sales lines  : {N_SALES:,}")
print(f"Start date   : {START_DATE}")
print(f"End date     : {END_DATE}")
print(f"Random seed  : {RANDOM_SEED}")

print("\nData directories:")
print(f"Raw         : {DATA_RAW}")
print(f"Processed   : {DATA_PROCESSED}")
print(f"Outputs     : {DATA_OUTPUTS}")

print("\nGenerator configuration loaded successfully.")


# ============================================================
# 6. REGION DIMENSION
# ============================================================

regions = [
    ("R01", "Dhaka", "Dhaka"),
    ("R02", "Chattogram", "Chattogram"),
    ("R03", "Rajshahi", "Rajshahi"),
    ("R04", "Khulna", "Khulna"),
    ("R05", "Sylhet", "Sylhet"),
    ("R06", "Rangpur", "Rangpur"),
    ("R07", "Barishal", "Barishal"),
    ("R08", "Mymensingh", "Mymensingh"),
]


dim_region = pd.DataFrame(
    regions,
    columns=[
        "region_id",
        "region_name",
        "division"
    ]
)


# ============================================================
# 7. SAVE REGION DATA
# ============================================================

region_file = DATA_RAW / "dim_region.csv"

dim_region.to_csv(
    region_file,
    index=False
)


# ============================================================
# 8. REGION VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("REGION DIMENSION")
print("=" * 60)

print(f"Number of regions: {len(dim_region)}")

print("\nRegion data:")
print(dim_region)

print(f"\nSaved to:")
print(region_file)

# ============================================================
# 9. PRODUCT DIMENSION
# ============================================================

product_catalog = {
    "Electronics": {
        "Audio": [
            "Wireless Headphones",
            "Bluetooth Speaker",
            "Earbuds",
            "Soundbar",
            "Wired Headphones"
        ],
        "Accessories": [
            "USB-C Cable",
            "Wireless Mouse",
            "Mechanical Keyboard",
            "Laptop Stand",
            "Power Bank"
        ],
        "Computing": [
            "Laptop",
            "Desktop Monitor",
            "External SSD",
            "Webcam",
            "USB Hub"
        ]
    },

    "Furniture": {
        "Office": [
            "Office Chair",
            "Computer Desk",
            "Office Table",
            "Filing Cabinet",
            "Bookshelf"
        ],
        "Home": [
            "Sofa",
            "Coffee Table",
            "Dining Table",
            "Dining Chair",
            "TV Stand"
        ],
        "Storage": [
            "Storage Cabinet",
            "Plastic Drawer",
            "Storage Box",
            "Shoe Rack",
            "Wardrobe"
        ]
    },

    "Grocery": {
        "Beverages": [
            "Mineral Water",
            "Soft Drink",
            "Fruit Juice",
            "Instant Coffee",
            "Tea Pack"
        ],
        "Snacks": [
            "Potato Chips",
            "Biscuits",
            "Chocolate",
            "Nuts",
            "Cereal Bar"
        ],
        "Staples": [
            "Rice",
            "Lentils",
            "Cooking Oil",
            "Sugar",
            "Flour"
        ]
    },

    "Fashion": {
        "Mens": [
            "Casual Shirt",
            "Formal Shirt",
            "T-Shirt",
            "Jeans",
            "Polo Shirt"
        ],
        "Womens": [
            "Kurti",
            "Saree",
            "Salwar Kameez",
            "Women's Top",
            "Women's Jeans"
        ],
        "Footwear": [
            "Running Shoes",
            "Formal Shoes",
            "Sneakers",
            "Sandals",
            "Casual Shoes"
        ]
    },

    "Home Appliances": {
        "Kitchen": [
            "Electric Kettle",
            "Rice Cooker",
            "Blender",
            "Microwave Oven",
            "Electric Stove"
        ],
        "Cleaning": [
            "Vacuum Cleaner",
            "Electric Mop",
            "Steam Cleaner",
            "Handheld Vacuum",
            "Floor Polisher"
        ],
        "Small Appliances": [
            "Table Fan",
            "Air Purifier",
            "Room Heater",
            "Humidifier",
            "Air Cooler"
        ]
    }
}

# ============================================================
# 10. GENERATE PRODUCT RECORDS
# ============================================================

products = []

product_number = 1

for category, subcategories in product_catalog.items():

    for subcategory, product_names in subcategories.items():

        for product_name in product_names:

            product_id = f"P{product_number:04d}"

            brand = rng.choice(
                ["Brand A", "Brand B", "Brand C", "Brand D", "Brand E"]
            )

            supplier_id = f"SUP{rng.integers(1, 11):03d}"

            products.append(
                {
                    "product_id": product_id,
                    "product_name": product_name,
                    "category": category,
                    "subcategory": subcategory,
                    "brand": brand,
                    "supplier_id": supplier_id
                }
            )

            product_number += 1


dim_product = pd.DataFrame(products)

# ============================================================
# 11. GENERATE PRODUCT PRICING
# ============================================================

dim_product["unit_cost"] = np.round(
    rng.uniform(100, 15000, size=len(dim_product)),
    2
)

dim_product["standard_price"] = np.round(
    dim_product["unit_cost"] * rng.uniform(
        1.20,
        1.80,
        size=len(dim_product)
    ),
    2
)

# ============================================================
# 12. PRODUCT POPULARITY
# ============================================================

dim_product["popularity"] = rng.choice(
    ["High", "Medium", "Low"],
    size=len(dim_product),
    p=[0.20, 0.50, 0.30]
)

# ============================================================
# 13. SAVE PRODUCT DATA
# ============================================================

product_file = DATA_RAW / "dim_product.csv"

dim_product.to_csv(
    product_file,
    index=False
)

# ============================================================
# 14. PRODUCT VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PRODUCT DIMENSION")
print("=" * 60)

print(f"Number of products: {len(dim_product)}")

print("\nFirst 10 products:")
print(
    dim_product.head(10).to_string(index=False)
)

print("\nProducts by category:")
print(
    dim_product["category"].value_counts()
)

print("\nProducts by popularity:")
print(
    dim_product["popularity"].value_counts()
)

print(f"\nSaved to:")
print(product_file)

# ============================================================
# 15. CUSTOMER DIMENSION
# ============================================================

cities_by_region = {
    "R01": ["Dhaka", "Gazipur", "Narayanganj"],
    "R02": ["Chattogram", "Cox's Bazar", "Cumilla"],
    "R03": ["Rajshahi", "Pabna", "Natore"],
    "R04": ["Khulna", "Jessore", "Satkhira"],
    "R05": ["Sylhet", "Moulvibazar", "Habiganj"],
    "R06": ["Rangpur", "Dinajpur", "Kurigram"],
    "R07": ["Barishal", "Pirojpur", "Bhola"],
    "R08": ["Mymensingh", "Jamalpur", "Netrokona"],
}

# ============================================================
# 16. GENERATE CUSTOMER RECORDS
# ============================================================

customers = []

region_ids = dim_region["region_id"].tolist()

# ------------------------------------------------------------
# Customer signup groups
# ------------------------------------------------------------
# 75% of customers already existed before the historical
# analysis period.
#
# 20% are acquired during 2024.
#
# 5% are acquired during 2025.
#
# This creates an established customer base while still
# allowing customer acquisition during the analysis period.

signup_group = rng.choice(
    [
        "Existing",
        "New_2024",
        "New_2025",
    ],
    size=N_CUSTOMERS,
    p=[
        0.75,
        0.20,
        0.05,
    ],
)

existing_dates = pd.date_range(
    "2023-01-01",
    "2023-12-31",
    freq="D",
)

new_2024_dates = pd.date_range(
    "2024-01-01",
    "2024-12-31",
    freq="D",
)

new_2025_dates = pd.date_range(
    "2025-01-01",
    "2025-12-31",
    freq="D",
)

for customer_number in range(1, N_CUSTOMERS + 1):

    customer_id = f"C{customer_number:04d}"

    region_id = rng.choice(
        region_ids
    )

    city = rng.choice(
        cities_by_region[region_id]
    )

    gender = rng.choice(
        ["Male", "Female"],
        p=[0.55, 0.45]
    )

    age = int(
        np.clip(
            rng.normal(34, 10),
            18,
            70
        )
    )

    # --------------------------------------------------------
    # Signup date
    # --------------------------------------------------------

    group = signup_group[
        customer_number - 1
    ]

    if group == "Existing":

        signup_date = pd.Timestamp(
            rng.choice(existing_dates)
        )

    elif group == "New_2024":

        signup_date = pd.Timestamp(
            rng.choice(new_2024_dates)
        )

    else:

        signup_date = pd.Timestamp(
            rng.choice(new_2025_dates)
        )

    customer_type = rng.choice(
        ["Individual", "Business"],
        p=[0.90, 0.10]
    )

    behavior_profile = rng.choice(
        [
            "Frequent",
            "Regular",
            "Occasional",
            "One-Time"
        ],
        p=[
            0.15,
            0.35,
            0.35,
            0.15
        ]
    )

    customers.append(
        {
            "customer_id": customer_id,
            "customer_name": f"Customer {customer_number:04d}",
            "gender": gender,
            "age": age,
            "city": city,
            "region_id": region_id,
            "signup_date": signup_date,
            "customer_type": customer_type,
            "behavior_profile": behavior_profile
        }
    )


dim_customer = pd.DataFrame(
    customers
)


# ============================================================
# 16A. CUSTOMER SIGNUP VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER SIGNUP DATE DISTRIBUTION")
print("=" * 60)

print(
    pd.Series(signup_group)
    .value_counts()
)

print(
    "\nSignup date range:"
)

print(
    dim_customer["signup_date"].min(),
    "to",
    dim_customer["signup_date"].max()
)

# ============================================================
# 17. SAVE CUSTOMER DATA
# ============================================================

customer_file = DATA_RAW / "dim_customer.csv"

dim_customer.to_csv(
    customer_file,
    index=False
)

# ============================================================
# 18. CUSTOMER VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER DIMENSION")
print("=" * 60)

print(f"Number of customers: {len(dim_customer)}")

print("\nFirst 10 customers:")
print(
    dim_customer.head(10).to_string(index=False)
)

print("\nCustomers by region:")
print(
    dim_customer["region_id"].value_counts().sort_index()
)

print("\nCustomers by behavior profile:")
print(
    dim_customer["behavior_profile"].value_counts()
)

print("\nCustomers by type:")
print(
    dim_customer["customer_type"].value_counts()
)

print(f"\nSaved to:")
print(customer_file)

# ============================================================
# 19. DATE DIMENSION
# ============================================================

date_range = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="D"
)


dim_date = pd.DataFrame(
    {
        "date": date_range
    }
)


# ============================================================
# 20. DATE ATTRIBUTES
# ============================================================

dim_date["year"] = dim_date["date"].dt.year

dim_date["quarter"] = (
    "Q" + dim_date["date"].dt.quarter.astype(str)
)

dim_date["month_number"] = (
    dim_date["date"].dt.month
)

dim_date["month_name"] = (
    dim_date["date"].dt.month_name()
)

dim_date["week_number"] = (
    dim_date["date"].dt.isocalendar().week.astype(int)
)

dim_date["day"] = (
    dim_date["date"].dt.day
)

dim_date["day_name"] = (
    dim_date["date"].dt.day_name()
)

dim_date["is_weekend"] = (
    dim_date["date"].dt.dayofweek >= 5
).astype(int)

# ============================================================
# 21. MONTH-YEAR
# ============================================================

dim_date["month_year"] = (
    dim_date["date"].dt.strftime("%Y-%m")
)

# ============================================================
# 22. SAVE DATE DATA
# ============================================================

date_file = DATA_RAW / "dim_date.csv"

dim_date.to_csv(
    date_file,
    index=False
)

# ============================================================
# 23. DATE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("DATE DIMENSION")
print("=" * 60)

print(f"Number of dates: {len(dim_date)}")

print("\nFirst 5 dates:")
print(
    dim_date.head().to_string(index=False)
)

print("\nLast 5 dates:")
print(
    dim_date.tail().to_string(index=False)
)

print("\nYear distribution:")
print(
    dim_date["year"].value_counts().sort_index()
)

print("\nWeekend days:")
print(
    dim_date["is_weekend"].value_counts()
)

print(f"\nSaved to:")
print(date_file)

# ============================================================
# 24. SALES DATE WEIGHTS
# ============================================================

# Create a working copy of the date dimension
sales_dates = dim_date.copy()

# ============================================================
# 25. TREND FACTOR
# ============================================================

# Gradual upward business growth over the 2-year period
sales_dates["trend_factor"] = np.linspace(
    1.00,
    1.20,
    len(sales_dates)
)

# ============================================================
# 26. MONTH SEASONALITY
# ============================================================

month_seasonality = {
    1: 0.90,
    2: 0.95,
    3: 1.00,
    4: 1.00,
    5: 1.05,
    6: 1.00,
    7: 1.00,
    8: 1.05,
    9: 1.00,
    10: 1.10,
    11: 1.25,
    12: 1.20,
}

sales_dates["month_factor"] = (
    sales_dates["month_number"]
    .map(month_seasonality)
)

# ============================================================
# 27. WEEKEND FACTOR
# ============================================================

sales_dates["weekend_factor"] = np.where(
    sales_dates["is_weekend"] == 1,
    1.15,
    1.00
)

# ============================================================
# 28. CONTROLLED ANOMALIES / PROMOTION DAYS
# ============================================================

sales_dates["anomaly_factor"] = 1.00

anomaly_dates = [
    "2024-11-11",
    "2024-12-12",
    "2025-11-11",
    "2025-12-12",
]

sales_dates.loc[
    sales_dates["date"].isin(
        pd.to_datetime(anomaly_dates)
    ),
    "anomaly_factor"
] = 1.50

# ============================================================
# 29. COMBINED SALES WEIGHT
# ============================================================

sales_dates["sales_weight"] = (
    sales_dates["trend_factor"]
    * sales_dates["month_factor"]
    * sales_dates["weekend_factor"]
    * sales_dates["anomaly_factor"]
)

# ============================================================
# 30. VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("SALES DATE WEIGHTS")
print("=" * 60)

print("\nDate-weight sample:")
print(
    sales_dates[
        [
            "date",
            "month_factor",
            "weekend_factor",
            "trend_factor",
            "anomaly_factor",
            "sales_weight",
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nHighest sales-weight dates:")

print(
    sales_dates[
        [
            "date",
            "sales_weight"
        ]
    ]
    .sort_values(
        "sales_weight",
        ascending=False
    )
    .head(10)
    .to_string(index=False)
)

print("\nSales weight statistics:")

print(
    sales_dates["sales_weight"].describe()
)

# ============================================================
# 31. CUSTOMER PURCHASE BEHAVIOR
# ============================================================

customer_sales = dim_customer.copy()

# ============================================================
# 32. BEHAVIOR-BASED PURCHASE WEIGHTS
# ============================================================

behavior_order_weight = {
    "Frequent": 1.00,
    "Regular": 0.55,
    "Occasional": 0.25,
    "One-Time": 0.08,
}

customer_sales["purchase_weight"] = (
    customer_sales["behavior_profile"]
    .map(behavior_order_weight)
)

# ============================================================
# 33. ACTIVE PERIOD
# ============================================================

analysis_start = pd.Timestamp(START_DATE)
analysis_end = pd.Timestamp(END_DATE)

# Customers who signed up before the analysis period
# are treated as active from the beginning of the
# historical analysis period.

effective_signup_date = (
    customer_sales["signup_date"]
    .clip(
        lower=analysis_start,
        upper=analysis_end,
    )
)

customer_sales["active_days"] = (
    analysis_end
    - effective_signup_date
).dt.days + 1

customer_sales["active_months"] = (
    customer_sales["active_days"] / 30.44
).clip(
    lower=1,
    upper=24,
).round(1)

# ============================================================
# 34. BASE ORDER INTENSITY
# ============================================================

# Base monthly order rates by customer behavior
monthly_order_rate = {
    "Frequent": 3.0,
    "Regular": 1.6,
    "Occasional": 0.70,
    "One-Time": 0.12,
}

customer_sales["monthly_order_rate"] = (
    customer_sales["behavior_profile"]
    .map(monthly_order_rate)
)

# ============================================================
# 35. EXPECTED ORDERS
# ============================================================

customer_sales["expected_orders"] = (
    customer_sales["active_months"]
    * customer_sales["monthly_order_rate"]
)

# ============================================================
# 36. GENERATE INITIAL ORDER COUNTS
# ============================================================

customer_sales["initial_orders"] = (
    rng.poisson(
        customer_sales["expected_orders"]
    )
)

# Ensure One-Time customers have at least one order
one_time_mask = (
    customer_sales["behavior_profile"] == "One-Time"
)

customer_sales.loc[
    one_time_mask,
    "initial_orders"
] = np.maximum(
    customer_sales.loc[
        one_time_mask,
        "initial_orders"
    ],
    1
)

# ============================================================
# 37. VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER PURCHASE BEHAVIOR")
print("=" * 60)

print("\nCustomer behavior distribution:")
print(
    customer_sales["behavior_profile"]
    .value_counts()
)

print("\nAverage active months by behavior:")
print(
    customer_sales
    .groupby("behavior_profile")["active_months"]
    .mean()
    .round(1)
)

print("\nAverage expected orders by behavior:")
print(
    customer_sales
    .groupby("behavior_profile")["expected_orders"]
    .mean()
    .round(1)
)

print("\nAverage initial orders by behavior:")
print(
    customer_sales
    .groupby("behavior_profile")["initial_orders"]
    .mean()
    .round(1)
)

print("\nTotal initial orders:")
print(
    customer_sales["initial_orders"].sum()
)

# ============================================================
# 38. GENERATE ORDERS
# ============================================================

orders = []

order_counter = 1

for _, customer in customer_sales.iterrows():

    customer_id = customer["customer_id"]
    signup_date = customer["signup_date"]
    n_orders = int(customer["initial_orders"])

    # Eligible dates for this customer
    eligible_dates = sales_dates[
        sales_dates["date"] >= signup_date
    ].copy()

    # Normalize sales weights into probabilities
    probabilities = (
        eligible_dates["sales_weight"]
        / eligible_dates["sales_weight"].sum()
    )

    # Generate order dates
    order_dates = rng.choice(
        eligible_dates["date"].values,
        size=n_orders,
        replace=True,
        p=probabilities.values
    )

    # Create orders
    for order_date in order_dates:

        orders.append(
            {
                "order_id": f"O{order_counter:06d}",
                "customer_id": customer_id,
                "order_date": pd.Timestamp(order_date),
                "region_id": customer["region_id"],
            }
        )

        order_counter += 1


orders_df = pd.DataFrame(orders)

# ============================================================
# 39. ORDER VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("ORDER GENERATION")
print("=" * 60)

print(f"Total orders: {len(orders_df):,}")

print("\nFirst 10 orders:")
print(
    orders_df
    .head(10)
    .to_string(index=False)
)

print("\nOrders by year:")
print(
    orders_df["order_date"]
    .dt.year
    .value_counts()
    .sort_index()
)

print("\nOrders by customer behavior:")

orders_behavior = orders_df.merge(
    customer_sales[
        [
            "customer_id",
            "behavior_profile"
        ]
    ],
    on="customer_id",
    how="left"
)

print(
    orders_behavior[
        "behavior_profile"
    ]
    .value_counts()
)

# ============================================================
# 40. SIGNUP-DATE VALIDATION
# ============================================================

signup_check = orders_df.merge(
    customer_sales[
        [
            "customer_id",
            "signup_date"
        ]
    ],
    on="customer_id",
    how="left"
)

invalid_orders = signup_check[
    signup_check["order_date"]
    < signup_check["signup_date"]
]

print("\nOrders before customer signup:")
print(len(invalid_orders))

if len(invalid_orders) == 0:
    print("Signup-date validation: PASSED")
else:
    print("Signup-date validation: FAILED")

# ============================================================
# 41. ORDER DATE RANGE
# ============================================================

print("\nOrder date range:")
print(
    orders_df["order_date"].min(),
    "to",
    orders_df["order_date"].max()
)

# ============================================================
# 42. GENERATE ORDER LINE COUNTS
# ============================================================

# Initial probability distribution for number of products
# contained in each order.
line_count_values = np.array([1, 2, 3, 4, 5])

line_count_probabilities = np.array(
    [0.10, 0.20, 0.30, 0.25, 0.15]
)

orders_df["line_count"] = rng.choice(
    line_count_values,
    size=len(orders_df),
    p=line_count_probabilities
)

# ============================================================
# 43. SCALE TO TARGET SALES LINES
# ============================================================

target_sales_lines = N_SALES

current_line_count = int(
    orders_df["line_count"].sum()
)

difference = (
    target_sales_lines
    - current_line_count
)

print("\n" + "=" * 60)
print("ORDER LINE GENERATION")
print("=" * 60)

print(
    f"Initial sales-line count: "
    f"{current_line_count:,}"
)

print(
    f"Target sales-line count: "
    f"{target_sales_lines:,}"
)

print(
    f"Difference: "
    f"{difference:,}"
)

# ============================================================
# 44. ADJUST LINE COUNTS
# ============================================================

if difference > 0:

    # Need more lines
    for _ in range(difference):

        index = rng.integers(
            0,
            len(orders_df)
        )

        if orders_df.loc[index, "line_count"] < 5:
            orders_df.loc[
                index,
                "line_count"
            ] += 1

elif difference < 0:

    # Need fewer lines
    for _ in range(abs(difference)):

        eligible_indices = orders_df.index[
            orders_df["line_count"] > 1
        ]

        index = rng.choice(
            eligible_indices
        )

        orders_df.loc[
            index,
            "line_count"
        ] -= 1

# ============================================================
# 45. FINAL VALIDATION
# ============================================================

final_line_count = int(
    orders_df["line_count"].sum()
)

print(
    f"\nFinal sales-line count: "
    f"{final_line_count:,}"
)

print("\nLine-count distribution:")

print(
    orders_df["line_count"]
    .value_counts()
    .sort_index()
)

print("\nAverage lines per order:")

print(
    round(
        orders_df["line_count"].mean(),
        2
    )
)

if final_line_count == target_sales_lines:
    print(
        "\nSales-line target validation: PASSED"
    )
else:
    print(
        "\nSales-line target validation: FAILED"
    )

print(
    orders_df["order_date"].min(),
    "to",
    orders_df["order_date"].max()
)

# ============================================================
# 46. PREPARE PRODUCT SALES WEIGHTS
# ============================================================

product_sales = dim_product.copy()

product_popularity_weight = {
    "High": 3.0,
    "Medium": 1.5,
    "Low": 0.7,
}

product_sales["sales_weight"] = (
    product_sales["popularity"]
    .map(product_popularity_weight)
)

# Normalize weights into probabilities
product_probabilities = (
    product_sales["sales_weight"]
    / product_sales["sales_weight"].sum()
)

# ============================================================
# 47. EXPAND ORDERS INTO SALES LINES
# ============================================================

sales_lines = []

sales_counter = 1

for _, order in orders_df.iterrows():

    n_lines = int(order["line_count"])

    selected_products = rng.choice(
        product_sales["product_id"].values,
        size=n_lines,
        replace=False,
        p=product_probabilities.values
    )

    for product_id in selected_products:

        sales_lines.append(
            {
                "sales_id": f"S{sales_counter:06d}",
                "order_id": order["order_id"],
                "order_date": order["order_date"],
                "customer_id": order["customer_id"],
                "product_id": product_id,
                "region_id": order["region_id"],
            }
        )

        sales_counter += 1

# Convert to DataFrame
fact_sales = pd.DataFrame(sales_lines)

# ============================================================
# 48. PRODUCT ASSIGNMENT VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PRODUCT ASSIGNMENT")
print("=" * 60)

print(
    f"Total sales lines: "
    f"{len(fact_sales):,}"
)

print("\nFirst 10 sales lines:")

print(
    fact_sales
    .head(10)
    .to_string(index=False)
)

print("\nUnique orders:")
print(
    fact_sales["order_id"].nunique()
)

print("\nUnique customers:")
print(
    fact_sales["customer_id"].nunique()
)

print("\nUnique products:")
print(
    fact_sales["product_id"].nunique()
)

print("\nProduct popularity distribution:")

product_check = fact_sales.merge(
    product_sales[
        [
            "product_id",
            "popularity"
        ]
    ],
    on="product_id",
    how="left"
)

print(
    product_check["popularity"]
    .value_counts()
)

# ============================================================
# 49. SALES-LINE VALIDATION
# ============================================================

if len(fact_sales) == N_SALES:
    print(
        "\nSales-line count validation: PASSED"
    )
else:
    print(
        "\nSales-line count validation: FAILED"
    )

if fact_sales["sales_id"].nunique() == len(fact_sales):
    print(
        "Sales ID uniqueness validation: PASSED"
    )
else:
    print(
        "Sales ID uniqueness validation: FAILED"
    )

if fact_sales["order_id"].nunique() == len(orders_df):
    print(
        "Order relationship validation: PASSED"
    )
else:
    print(
        "Order relationship validation: FAILED"
    )

# ============================================================
# 50. MERGE PRODUCT INFORMATION
# ============================================================

fact_sales = fact_sales.merge(
    product_sales[
        [
            "product_id",
            "category",
            "subcategory",
            "brand",
            "unit_cost",
            "standard_price",
            "popularity",
        ]
    ],
    on="product_id",
    how="left"
)

# ============================================================
# 51. MERGE CUSTOMER INFORMATION
# ============================================================

fact_sales = fact_sales.merge(
    customer_sales[
        [
            "customer_id",
            "behavior_profile",
            "customer_type",
        ]
    ],
    on="customer_id",
    how="left"
)

# ============================================================
# 52. VALIDATE LOOKUPS
# ============================================================

print("\n" + "=" * 60)
print("PRODUCT & CUSTOMER LOOKUPS")
print("=" * 60)

print("\nMissing product records:")

print(
    fact_sales["standard_price"]
    .isna()
    .sum()
)

print("\nMissing customer records:")

print(
    fact_sales["behavior_profile"]
    .isna()
    .sum()
)

# ============================================================
# 53. GENERATE QUANTITY
# ============================================================

# Base quantity by product popularity
quantity_lambda = {
    "High": 2.4,
    "Medium": 1.8,
    "Low": 1.3,
}

fact_sales["quantity_lambda"] = (
    fact_sales["popularity"]
    .map(quantity_lambda)
)

# Business customers tend to purchase larger quantities
fact_sales.loc[
    fact_sales["customer_type"] == "Business",
    "quantity_lambda"
] *= 1.25

# Generate quantity using Poisson distribution
fact_sales["quantity"] = (
    rng.poisson(
        fact_sales["quantity_lambda"]
    ) + 1
)

# Limit extreme quantities
fact_sales["quantity"] = (
    fact_sales["quantity"]
    .clip(lower=1, upper=10)
    .astype(int)
)

# ============================================================
# 54. QUANTITY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("QUANTITY GENERATION")
print("=" * 60)

print("\nQuantity statistics:")

print(
    fact_sales["quantity"]
    .describe()
)

print("\nAverage quantity by popularity:")

print(
    fact_sales
    .groupby("popularity")["quantity"]
    .mean()
    .round(2)
)

print("\nAverage quantity by customer type:")

print(
    fact_sales
    .groupby("customer_type")["quantity"]
    .mean()
    .round(2)
)

print("\nQuantity distribution:")

print(
    fact_sales["quantity"]
    .value_counts()
    .sort_index()
)

# ============================================================
# 55. GENERATE UNIT PRICE
# ============================================================

# Random price variation around the standard price
price_multiplier = rng.uniform(
    0.95,
    1.05,
    size=len(fact_sales)
)

fact_sales["unit_price"] = (
    fact_sales["standard_price"]
    * price_multiplier
)

# Round to two decimal places
fact_sales["unit_price"] = (
    fact_sales["unit_price"]
    .round(2)
)

# ============================================================
# 56. PRICE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("UNIT PRICE GENERATION")
print("=" * 60)

print("\nUnit price statistics:")

print(
    fact_sales["unit_price"]
    .describe()
)

print("\nSample prices:")

print(
    fact_sales[
        [
            "product_id",
            "standard_price",
            "unit_price"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nPrice below product cost:")

print(
    (
        fact_sales["unit_price"]
        < fact_sales["unit_cost"]
    )
    .sum()
)

# ============================================================
# 57. GENERATE PROMOTION FLAG
# ============================================================

# Start with a baseline promotion probability
promotion_probability = np.full(
    len(fact_sales),
    0.15
)

# Increase promotion probability during
# November and December
high_season_mask = (
    fact_sales["order_date"].dt.month.isin(
        [11, 12]
    )
)

promotion_probability[
    high_season_mask
] = 0.25

# Increase promotion probability on
# controlled anomaly / campaign dates
campaign_dates = pd.to_datetime(
    [
        "2024-11-11",
        "2024-12-12",
        "2025-11-11",
        "2025-12-12",
    ]
)

campaign_mask = (
    fact_sales["order_date"].isin(
        campaign_dates
    )
)

promotion_probability[
    campaign_mask
] = 0.60

# Generate promotion flag
fact_sales["promotion_flag"] = (
    rng.random(
        len(fact_sales)
    )
    < promotion_probability
).astype(int)

# ============================================================
# 58. GENERATE DISCOUNT PERCENTAGE
# ============================================================

fact_sales["discount_pct"] = 0.0

promotion_mask = (
    fact_sales["promotion_flag"] == 1
)

fact_sales.loc[
    promotion_mask,
    "discount_pct"
] = (
    rng.uniform(
        5.0,
        20.0,
        size=promotion_mask.sum()
    )
    .round(2)
)

# ============================================================
# 59. PROMOTION VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PROMOTION & DISCOUNT GENERATION")
print("=" * 60)

print("\nPromotion distribution:")

print(
    fact_sales["promotion_flag"]
    .value_counts()
    .rename(
        index={
            0: "No Promotion",
            1: "Promotion"
        }
    )
)

print("\nPromotion rate:")

print(
    round(
        fact_sales["promotion_flag"].mean() * 100,
        2
    ),
    "%"
)

print("\nDiscount statistics:")

print(
    fact_sales["discount_pct"]
    .describe()
)

print("\nDiscount among promotional transactions:")

print(
    fact_sales.loc[
        promotion_mask,
        "discount_pct"
    ].describe()
)

print("\nDiscount validation:")

invalid_discount = (
    (
        fact_sales["promotion_flag"] == 0
    )
    &
    (
        fact_sales["discount_pct"] > 0
    )
).sum()

print(
    f"Non-promotion rows with discount: "
    f"{invalid_discount}"
)

if invalid_discount == 0:
    print(
        "Discount consistency validation: PASSED"
    )
else:
    print(
        "Discount consistency validation: FAILED"
    )

# ============================================================
# 60. CALCULATE GROSS SALES
# ============================================================

fact_sales["gross_sales"] = (
    fact_sales["quantity"]
    * fact_sales["unit_price"]
)

# ============================================================
# 61. CALCULATE DISCOUNT AMOUNT
# ============================================================

fact_sales["discount_amount"] = (
    fact_sales["gross_sales"]
    * fact_sales["discount_pct"]
    / 100
)

# ============================================================
# 62. CALCULATE REVENUE
# ============================================================

fact_sales["revenue"] = (
    fact_sales["gross_sales"]
    - fact_sales["discount_amount"]
)

# ============================================================
# 63. CALCULATE COST
# ============================================================

fact_sales["cost"] = (
    fact_sales["quantity"]
    * fact_sales["unit_cost"]
)

# ============================================================
# 64. CALCULATE PROFIT
# ============================================================

fact_sales["profit"] = (
    fact_sales["revenue"]
    - fact_sales["cost"]
)

# ============================================================
# 65. CALCULATE PROFIT MARGIN
# ============================================================

fact_sales["profit_margin_pct"] = (
    fact_sales["profit"]
    / fact_sales["revenue"]
    * 100
)

# ============================================================
# 66. ROUND FINANCIAL VALUES
# ============================================================

financial_columns = [
    "unit_price",
    "gross_sales",
    "discount_amount",
    "revenue",
    "cost",
    "profit",
    "profit_margin_pct",
]

fact_sales[financial_columns] = (
    fact_sales[financial_columns]
    .round(2)
)

# ============================================================
# 67. FINANCIAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("REVENUE, COST & PROFIT")
print("=" * 60)

print("\nFinancial summary:")

print(
    fact_sales[
        [
            "gross_sales",
            "discount_amount",
            "revenue",
            "cost",
            "profit",
            "profit_margin_pct",
        ]
    ]
    .describe()
    .round(2)
)

print("\nTotal business metrics:")

print(
    f"Gross Sales : "
    f"{fact_sales['gross_sales'].sum():,.2f}"
)

print(
    f"Discount    : "
    f"{fact_sales['discount_amount'].sum():,.2f}"
)

print(
    f"Revenue     : "
    f"{fact_sales['revenue'].sum():,.2f}"
)

print(
    f"Cost        : "
    f"{fact_sales['cost'].sum():,.2f}"
)

print(
    f"Profit      : "
    f"{fact_sales['profit'].sum():,.2f}"
)

print(
    f"Profit Margin: "
    f"{fact_sales['profit'].sum() / fact_sales['revenue'].sum() * 100:.2f}%"
)

# ============================================================
# 68. FINANCIAL CONSISTENCY CHECK
# ============================================================

revenue_check = np.isclose(
    fact_sales["revenue"],
    (
        fact_sales["gross_sales"]
        - fact_sales["discount_amount"]
    ),
    atol=0.01
)

profit_check = np.isclose(
    fact_sales["profit"],
    (
        fact_sales["revenue"]
        - fact_sales["cost"]
    ),
    atol=0.01
)

print("\nFinancial validation:")

print(
    f"Revenue calculation errors: "
    f"{(~revenue_check).sum()}"
)

print(
    f"Profit calculation errors: "
    f"{(~profit_check).sum()}"
)

if revenue_check.all():
    print(
        "Revenue calculation validation: PASSED"
    )
else:
    print(
        "Revenue calculation validation: FAILED"
    )

if profit_check.all():
    print(
        "Profit calculation validation: PASSED"
    )
else:
    print(
        "Profit calculation validation: FAILED"
    )

# ============================================================
# 69. GENERATE PAYMENT METHOD
# ============================================================

payment_methods = [
    "Mobile Banking",
    "Card",
    "Cash",
    "Bank Transfer",
]

payment_probabilities = [
    0.35,
    0.30,
    0.20,
    0.15,
]

fact_sales["payment_method"] = rng.choice(
    payment_methods,
    size=len(fact_sales),
    p=payment_probabilities
)

# ============================================================
# 70. GENERATE SALES CHANNEL
# ============================================================

sales_channels = [
    "Online",
    "Store",
    "Marketplace",
]

channel_probabilities = [
    0.50,
    0.30,
    0.20,
]

fact_sales["sales_channel"] = rng.choice(
    sales_channels,
    size=len(fact_sales),
    p=channel_probabilities
)

# ============================================================
# 71. PAYMENT & CHANNEL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PAYMENT METHOD & SALES CHANNEL")
print("=" * 60)

print("\nPayment method distribution:")

print(
    fact_sales["payment_method"]
    .value_counts()
)

print("\nSales channel distribution:")

print(
    fact_sales["sales_channel"]
    .value_counts()
)

print("\nPayment method percentage:")

print(
    (
        fact_sales["payment_method"]
        .value_counts(normalize=True)
        * 100
    )
    .round(2)
)

print("\nSales channel percentage:")

print(
    (
        fact_sales["sales_channel"]
        .value_counts(normalize=True)
        * 100
    )
    .round(2)
)

# ============================================================
# 72. FINAL FACT SALES TABLE
# ============================================================

fact_sales_final = fact_sales[
    [
        "sales_id",
        "order_id",
        "order_date",
        "customer_id",
        "product_id",
        "region_id",
        "quantity",
        "unit_price",
        "discount_pct",
        "revenue",
        "cost",
        "profit",
        "payment_method",
        "sales_channel",
        "promotion_flag",
    ]
].copy()

# ============================================================
# 73. SORT FACT SALES
# ============================================================

fact_sales_final = (
    fact_sales_final
    .sort_values(
        [
            "order_date",
            "order_id",
            "sales_id",
        ]
    )
    .reset_index(drop=True)
)

# ============================================================
# 74. FINAL DATA TYPES
# ============================================================

fact_sales_final["order_date"] = pd.to_datetime(
    fact_sales_final["order_date"]
)

fact_sales_final["quantity"] = (
    fact_sales_final["quantity"]
    .astype(int)
)

fact_sales_final["promotion_flag"] = (
    fact_sales_final["promotion_flag"]
    .astype(int)
)

# ============================================================
# 75. FINAL FACT SALES VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL FACT SALES")
print("=" * 60)

print(
    f"Rows: "
    f"{len(fact_sales_final):,}"
)

print(
    f"Columns: "
    f"{len(fact_sales_final.columns)}"
)

print("\nColumns:")

print(
    fact_sales_final.columns.tolist()
)

print("\nFirst 10 rows:")

print(
    fact_sales_final
    .head(10)
    .to_string(index=False)
)

print("\nData types:")

print(
    fact_sales_final.dtypes
)

# ============================================================
# 76. NULL VALIDATION
# ============================================================

print("\nMissing values by column:")

print(
    fact_sales_final
    .isna()
    .sum()
)

# ============================================================
# 77. KEY VALIDATION
# ============================================================

print("\nKey validation:")

print(
    "Unique sales IDs:",
    fact_sales_final["sales_id"].nunique()
)

print(
    "Unique order IDs:",
    fact_sales_final["order_id"].nunique()
)

print(
    "Unique customers:",
    fact_sales_final["customer_id"].nunique()
)

print(
    "Unique products:",
    fact_sales_final["product_id"].nunique()
)

print(
    "Unique regions:",
    fact_sales_final["region_id"].nunique()
)

# ============================================================
# 78. FINAL BUSINESS VALIDATION
# ============================================================

print("\nBusiness validation:")

print(
    "Negative quantity:",
    (
        fact_sales_final["quantity"] <= 0
    ).sum()
)

print(
    "Negative revenue:",
    (
        fact_sales_final["revenue"] < 0
    ).sum()
)

print(
    "Negative cost:",
    (
        fact_sales_final["cost"] < 0
    ).sum()
)

print(
    "Negative profit:",
    (
        fact_sales_final["profit"] < 0
    ).sum()
)

print(
    "Promotion with zero discount:",
    (
        (
            fact_sales_final["promotion_flag"] == 1
        )
        &
        (
            fact_sales_final["discount_pct"] == 0
        )
    ).sum()
)

# ============================================================
# 79. SAVE FACT SALES CSV
# ============================================================

fact_sales_csv = DATA_RAW / "fact_sales.csv"

fact_sales_final.to_csv(
    fact_sales_csv,
    index=False
)

# ============================================================
# 80. PARQUET EXPORT
# ============================================================

# Parquet export is temporarily disabled because
# the local Windows environment is blocking a pyarrow DLL.
# CSV is sufficient for V1.

print("\nParquet export skipped.")
print("Reason: local pyarrow DLL restriction.")
print("V1 will use CSV files.")

# ============================================================
# 81. FILE INFORMATION
# ============================================================

print("\nSaved Fact Sales CSV:")
print(fact_sales_csv)














