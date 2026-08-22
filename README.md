# MLOps Training 2026/2027 — Task 1

## Get the Data Into a Database

A hands-on MLOps task focused on understanding the Olist e-commerce dataset, loading the data into a relational PostgreSQL database, and validating the database and table relationships.

**Status: Completed**

---

## Project Overview

The objective of Task 1 was to:

- Understand the Olist dataset and its relationships.
- Load the CSV files into PostgreSQL.
- Run PostgreSQL locally using Docker.
- Automate data ingestion using Python.
- Execute SQL queries and JOIN operations.
- Validate the relationships between the main tables.
- Understand the future machine learning problem.

EDA and Machine Learning were **not required** for this task.

---

## Project Structure

```text
olist_postgres_p1/
│
├── archive/
│   └── CSV dataset files
│
├── scripts/
│   └── ingest.py
│
├── sql/
│   └── validation.sql
│
├── .gitignore
├── MLOps_Task1.pdf
├── Olist_Dataset_Introduction.pdf
└── README.md
```

> The raw CSV dataset is intentionally excluded from GitHub through `.gitignore`.

---

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains the following tables:

| Table | Description |
|---|---|
| `customers` | Customer information |
| `orders` | Order information and timestamps |
| `order_items` | Products contained in each order |
| `order_payments` | Payment information |
| `order_reviews` | Customer reviews |
| `products` | Product information |
| `sellers` | Seller information |
| `geolocation` | Brazilian geographic information |
| `product_category_translation` | Portuguese-to-English category translation |

---

## Table Relationships

The main identifiers used to connect the tables are:

- `order_id`
- `customer_id`
- `product_id`
- `seller_id`

### Relationship Diagram

```text
                     ┌─────────────────┐
                     │    customers    │
                     ├─────────────────┤
                     │ customer_id     │
                     └────────┬────────┘
                              │
                              │ customer_id
                              ▼
                     ┌────────┴────────┐
                     │     orders      │
                     ├─────────────────┤
                     │ order_id        │
                     │ customer_id     │
                     └──────┬─────┬────┘
                            │     │
                 order_id   │     │ order_id
                            │     │
                 ┌──────────▼─┐ ┌─▼────────────────┐
                 │order_items │ │  order_payments  │
                 ├────────────┤ └──────────────────┘
                 │ order_id   │
                 │ product_id │
                 │ seller_id  │
                 └──────┬─────┘
                        │
                ┌───────┴────────┐
                │                │
          product_id         seller_id
                │                │
                ▼                ▼
        ┌─────────────┐   ┌─────────────┐
        │  products   │   │   sellers   │
        └─────────────┘   └─────────────┘
```

Reviews are connected to orders through:

```text
orders.order_id
       │
       ▼
order_reviews.order_id
```

Product category translation:

```text
products.product_category_name
               │
               ▼
product_category_translation.product_category_name
```

Geolocation data is related to geographic ZIP code prefixes.

---

## Future Machine Learning Problem

The future ML problem is a **binary classification task**:

> Predict whether an order will be delivered late or on time.

The target can be conceptually defined as:

```text
Actual delivery date > Estimated delivery date
                    │
                    ▼
                 LATE = 1
```

```text
Actual delivery date <= Estimated delivery date
                    │
                    ▼
               ON_TIME = 0
```

### Data Leakage Warning

The actual delivery date must **not** be used as an input feature when making a prediction because it is future information.

It can be used to create the training target, but it must not be used as a predictive feature.

---

## Technologies Used

- Python
- Pandas
- SQLAlchemy
- Psycopg2
- PostgreSQL
- Docker
- WSL Ubuntu
- SQL
- Git / GitHub

---

## Environment

The project was developed inside **WSL Ubuntu**.

### Python Environment

A dedicated virtual environment was created:

```text
.venv/
```

Installed packages include:

```text
pandas
SQLAlchemy
psycopg2-binary
```

---

## PostgreSQL Setup

PostgreSQL was run using Docker.

### Container

```text
olist_postgres
```

### Database

```text
olist_db
```

### User

```text
olist_user
```

### Port

```text
5432
```

The database was successfully verified with:

```bash
docker ps
```

and a PostgreSQL connection test.

---

## Data Ingestion

Data ingestion was automated using:

```text
scripts/ingest.py
```

The ingestion script:

1. Connects to PostgreSQL.
2. Verifies the database connection.
3. Checks that the CSV files exist.
4. Loads the CSV files using Pandas.
5. Converts important columns to appropriate data types.
6. Loads the data into PostgreSQL.
7. Verifies the number of rows after insertion.
8. Reports the loading status of every table.

### Run Ingestion

```bash
python scripts/ingest.py
```

Successful execution ends with:

```text
All tables loaded successfully.
```

---

## Database Tables

The PostgreSQL database contains 9 tables:

```text
customers
geolocation
order_items
order_payments
order_reviews
orders
product_category_translation
products
sellers
```

---

## Dataset Row Counts

The final row counts loaded into PostgreSQL are:

| Table | Rows |
|---|---:|
| `customers` | 99,441 |
| `geolocation` | 1,000,163 |
| `order_items` | 112,650 |
| `order_payments` | 103,886 |
| `order_reviews` | 99,224 |
| `orders` | 99,441 |
| `products` | 32,951 |
| `sellers` | 3,095 |
| `product_category_translation` | 71 |

All loaded row counts were verified after ingestion.

---

## SQL Validation

Database validation was implemented in:

```text
sql/validation.sql
```

It checks:

- Available database tables.
- Table row counts.
- Basic `SELECT` queries.
- JOIN operations.
- Relationship integrity.
- Duplicate review IDs.
- Delivery statistics.

### Run Validation

From the project root:

```bash
docker exec -i olist_postgres psql \
  -U olist_user \
  -d olist_db \
  < sql/validation.sql
```

---

## Query Testing

### Basic Query

```sql
SELECT *
FROM orders
LIMIT 5;
```

This successfully returned order records.

---

## JOIN Validation

### Orders + Customers

```sql
SELECT
    o.order_id,
    o.order_status,
    o.order_purchase_timestamp,
    c.customer_city,
    c.customer_state
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
LIMIT 10;
```

This validated the relationship:

```text
orders.customer_id
        │
        ▼
customers.customer_id
```

### Orders + Order Items

```sql
SELECT
    o.order_id,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
LIMIT 10;
```

This validated:

```text
orders.order_id
       │
       ▼
order_items.order_id
```

---

## Relationship Validation Results

The following integrity checks were performed:

| Check | Result |
|---|---:|
| Orders without customers | `0` |
| Order items without orders | `0` |
| Order items without products | `0` |
| Order items without sellers | `0` |
| Payments without orders | `0` |

The tested core relationships are therefore consistent.

---

## Data Quality Observation

The `order_reviews` table contains:

```text
Total rows:       99,224
Unique review_id: 98,410
Duplicate IDs:       814
```

The duplicate `review_id` values were intentionally **not removed**.

### Reason

Task 1 focuses on:

- Data ingestion
- Database storage
- SQL queries
- Relationship validation

It does not require data cleaning.

Removing records without understanding why the IDs are duplicated could alter the original dataset.

This issue is therefore documented for possible investigation in a future task.

---

## Delivery Data Validation

The validation queries produced the following results:

| Metric | Count |
|---|---:|
| Delivered orders | 96,478 |
| Delivered orders with actual delivery date | 96,470 |
| Late delivered orders | 7,826 |
| On-time delivered orders | 88,644 |

These results confirm that the dataset contains the information required to construct the future delivery-delay classification target.

---

## Data Flow

```text
             CSV DATA
                │
                ▼
          archive/*.csv
                │
                ▼
       ┌─────────────────┐
       │  ingest.py      │
       │ Python / Pandas │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │   PostgreSQL    │
       │    olist_db     │
       └────────┬────────┘
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
   SQL Queries      SQL Validation
                         │
                         ▼
                  validation.sql
                         │
                         ▼
                 Verified Database
```

---

## Problems Encountered

### 1. PowerShell Docker Command Formatting

The initial Docker command used Linux line continuation:

```text
\
```

inside Windows PowerShell.

PowerShell does not use `\` for line continuation, which caused:

```text
docker: invalid reference format
```

The PostgreSQL container was then created correctly from WSL, where the Linux syntax is valid.

---

### 2. WSL and Windows Project Path

The Windows path:

```text
D:\Dev\Projects
```

contains a symbolic link pointing to the WSL project directory.

Direct access through:

```text
/mnt/d/Dev/Projects
```

caused an `Input/output error`.

The actual project path inside WSL was used instead:

```text
/home/abdul/Dev/projects/Machine_Learning/olist_postgres_p1
```

---

### 3. SQLAlchemy dtype Error

An early version of `ingest.py` failed with:

```text
ValueError:
The type of customer_id is not a SQLAlchemy type
```

The issue was caused by passing incompatible type definitions to `pandas.to_sql()`.

The ingestion script was then updated to use actual SQLAlchemy types such as:

```text
Text
BigInteger
Float
DateTime
```

After the fix, all tables loaded successfully.

---

## What I Practiced

This task provided hands-on practice with:

- Docker fundamentals.
- Running PostgreSQL locally.
- PostgreSQL database connections.
- Python database connectivity.
- Pandas CSV ingestion.
- SQLAlchemy.
- SQL `SELECT`.
- SQL `JOIN`.
- Relational table relationships.
- Row-count validation.
- Data integrity validation.
- Data quality investigation.
- Basic data leakage awareness.
- Git and GitHub workflow.

---

## Final Task Checklist

- [x] Dataset downloaded and available locally.
- [x] CSV files verified.
- [x] PostgreSQL running locally.
- [x] PostgreSQL running inside Docker.
- [x] Database created.
- [x] All 9 tables loaded.
- [x] Row counts verified.
- [x] Tables queried successfully.
- [x] `orders` → `customers` JOIN tested.
- [x] `orders` → `order_items` JOIN tested.
- [x] Core relationships validated.
- [x] Data quality observation documented.
- [x] Delivery target logic understood.
- [x] No unnecessary EDA performed.
- [x] Python ingestion automated.
- [x] SQL validation script created.
- [x] Task requirements completed.

---

## Final Status

### Task 1 — COMPLETED

The Olist dataset is successfully available in a local PostgreSQL database running through Docker.

The database can be queried successfully, the main table relationships have been tested and validated, and the future machine learning problem has been understood.

The project is ready for the next MLOps training task.
