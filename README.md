============================================================
MLOps Training 2026/2027
Task 1 - Get the Data Into a Database
============================================================

Project:
Olist E-Commerce Dataset

Database:
PostgreSQL

Container:
Docker

Status:
COMPLETED


============================================================
1. TASK OBJECTIVE
============================================================

The goal of Task 1 was to understand the Olist dataset, load the
CSV files into a relational PostgreSQL database, test the database
connection, run SQL queries and joins, and validate the relationships
between the main tables.

The task was intentionally limited to data ingestion and database
validation.

No EDA or Machine Learning model was required at this stage.


============================================================
2. PROJECT STRUCTURE
============================================================

The project is located at:

~/Dev/projects/Machine_Learning/olist_postgres_p1


Project structure:

olist_postgres_p1/
|
+-- archive/
|   +-- olist_customers_dataset.csv
|   +-- olist_geolocation_dataset.csv
|   +-- olist_order_items_dataset.csv
|   +-- olist_order_payments_dataset.csv
|   +-- olist_order_reviews_dataset.csv
|   +-- olist_orders_dataset.csv
|   +-- olist_products_dataset.csv
|   +-- olist_sellers_dataset.csv
|   +-- product_category_name_translation.csv
|
+-- scripts/
|   +-- ingest.py
|
+-- sql/
|   +-- validation.sql
|
+-- .venv/


============================================================
3. DATASET OVERVIEW
============================================================

The dataset is an e-commerce dataset from Olist, a Brazilian
e-commerce platform.

The dataset is divided into multiple related CSV files.

The main entities are:

1. Orders
2. Customers
3. Order Items
4. Payments
5. Reviews
6. Products
7. Sellers
8. Geolocation
9. Product Category Translation


============================================================
4. TABLE RELATIONSHIPS
============================================================

The main relationships are based on the following identifiers:

order_id
customer_id
product_id
seller_id


Relationship diagram:

                     +----------------+
                     |   customers    |
                     |----------------|
                     | customer_id    |
                     +-------+--------+
                             |
                             | customer_id
                             |
                             v
                     +-------+--------+
                     |     orders     |
                     |----------------|
                     | order_id       |
                     | customer_id    |
                     +---+--------+---+
                         |        |
              order_id   |        | order_id
                         |        |
                         v        v
                +--------+--+  +--+----------------+
                |order_items|  |  order_payments   |
                +-----+-----+  +-------------------+
                      |
             +--------+--------+
             |                 |
       product_id          seller_id
             |                 |
             v                 v
       +-----+------+    +-----+------+
       |  products  |    |  sellers   |
       +------------+    +------------+


Reviews are also connected to orders through:

orders.order_id
        |
        v
order_reviews.order_id


Geolocation is related to geographic ZIP code prefixes.

Product category translation is related to:

products.product_category_name
        |
        v
product_category_translation.product_category_name


============================================================
5. BUSINESS / ML PROBLEM
============================================================

The future machine learning problem is to predict whether an order
will be delivered late or on time.

The target can be derived from:

actual delivery date
        versus
estimated delivery date


Conceptually:

actual_delivery_date > estimated_delivery_date
                |
                v
             LATE = 1


actual_delivery_date <= estimated_delivery_date
                |
                v
           ON_TIME = 0


Important:

The actual delivery date must NOT be used as a feature when making
the prediction because it is future information.

It can be used to create the training target, but not as an input
feature for the model.


============================================================
6. ENVIRONMENT
============================================================

The project was executed inside WSL Ubuntu.

Python environment:

.venv

Python packages used for ingestion:

pandas
SQLAlchemy
psycopg2-binary


PostgreSQL was running inside Docker.

Docker container:

olist_postgres


Database:

olist_db


Database user:

olist_user


Port:

5432


============================================================
7. DOCKER DATABASE
============================================================

The PostgreSQL container was verified using:

docker ps


Result:

olist_postgres
Status: Up
Port: 5432 -> 5432


This confirmed that PostgreSQL was running locally and available
for the ingestion process.


============================================================
8. INGESTION PROCESS
============================================================

The ingestion process was automated using:

scripts/ingest.py


The script:

1. Connects to PostgreSQL.
2. Tests the database connection.
3. Checks that the CSV files exist.
4. Reads each CSV file.
5. Converts columns to appropriate data types.
6. Loads the data into PostgreSQL.
7. Verifies the number of rows after insertion.
8. Reports the result for every table.


The ingestion command:

python scripts/ingest.py


Final result:

All tables loaded successfully.


============================================================
9. DATABASE TABLES
============================================================

The database contains 9 tables:

customers
geolocation
order_items
order_payments
order_reviews
orders
product_category_translation
products
sellers


============================================================
10. ROW COUNTS
============================================================

The final row counts in PostgreSQL were:

customers
99,441

geolocation
1,000,163

order_items
112,650

order_payments
103,886

order_reviews
99,224

orders
99,441

products
32,951

sellers
3,095

product_category_translation
71


All row counts matched the source CSV files.


============================================================
11. SQL VALIDATION
============================================================

A validation file was created:

sql/validation.sql


It was executed using:

docker exec -i olist_postgres psql \
  -U olist_user \
  -d olist_db \
  < sql/validation.sql


The validation script checks:

- Existing tables
- Row counts
- Basic SELECT queries
- JOIN operations
- Relationship integrity
- Review ID duplication
- Delivery statistics


============================================================
12. QUERY TEST
============================================================

A basic query was tested:

SELECT *
FROM orders
LIMIT 5;


The query successfully returned order records.


============================================================
13. JOIN TEST
============================================================

A JOIN between orders and customers was tested:

orders
   |
   | customer_id
   v
customers


The query successfully returned:

order_id
order_status
order_purchase_timestamp
customer_city
customer_state


This confirmed that the main order/customer relationship works.


============================================================
14. SECOND JOIN TEST
============================================================

A second JOIN was tested between orders and order_items:

orders
   |
   | order_id
   v
order_items


The query successfully returned:

order_id
product_id
seller_id
price
freight_value


This confirmed another important relationship in the dataset.


============================================================
15. RELATIONSHIP VALIDATION
============================================================

The following checks were performed.

Orders without customers:

0


Order items without orders:

0


Order items without products:

0


Order items without sellers:

0


Payments without orders:

0


This means that all tested core relationships are valid.


============================================================
16. DATA QUALITY OBSERVATION
============================================================

The order_reviews table contains:

Total review rows:
99,224

Unique review IDs:
98,410

Duplicate review IDs:
814


This was recorded as a data quality observation.

The duplicate records were NOT deleted during Task 1.

Reason:

Task 1 is focused on ingestion and database validation, not data
cleaning. Removing records without understanding why the IDs are
duplicated could change the original dataset.

The issue can be investigated later if it becomes relevant to a
future task.


============================================================
17. DELIVERY DATA VALIDATION
============================================================

The validation queries showed:

Delivered orders:
96,478


Delivered orders with an actual delivery date:
96,470


Late delivered orders:
7,826


On-time delivered orders:
88,644


These numbers confirm that the dataset contains enough information
to define the future classification target.


============================================================
18. DATA FLOW
============================================================

The complete Task 1 data flow is:

CSV FILES
   |
   v
archive/
   |
   v
Python ingestion script
scripts/ingest.py
   |
   v
PostgreSQL
   |
   v
olist_db
   |
   +----------------------+
   |                      |
   v                      v
SQL Queries          SQL Validation
                       |
                       v
                  validation.sql
                       |
                       v
                Verified Database


============================================================
19. WHAT WAS LEARNED
============================================================

During this task I learned and practiced:

- Docker basics
- Running PostgreSQL inside Docker
- Connecting Python to PostgreSQL
- SQLAlchemy
- Pandas data ingestion
- Loading CSV data into relational tables
- SQL SELECT queries
- SQL JOIN operations
- Basic relational data validation
- Checking row counts
- Checking missing relationships
- Understanding primary identifiers
- Identifying data quality issues
- Understanding data leakage at a high level


============================================================
20. PROBLEMS ENCOUNTERED
============================================================

Problem 1:

The first version of ingest.py failed with:

ValueError:
The type of customer_id is not a SQLAlchemy type


Cause:

The dtype mapping passed to pandas.to_sql() was incorrect.


Solution:

The ingestion script was updated to use actual SQLAlchemy types such
as:

Text
BigInteger
Float
DateTime


After the fix, all tables were successfully loaded.


------------------------------------------------------------

Problem 2:

order_reviews contains duplicate review_id values.

Result:

814 duplicate review IDs.


Decision:

The records were kept unchanged and the issue was documented for
future data quality work.


============================================================
21. FINAL TASK CHECKLIST
============================================================

[✓] Dataset downloaded and available locally

[✓] CSV files verified

[✓] PostgreSQL running locally

[✓] PostgreSQL running inside Docker

[✓] Database created

[✓] All 9 tables loaded

[✓] Row counts verified

[✓] Tables queried successfully

[✓] JOIN between orders and customers tested

[✓] JOIN between orders and order_items tested

[✓] Core relationships validated

[✓] Data quality observation documented

[✓] Delivery target logic understood

[✓] No unnecessary EDA performed

[✓] Ingestion automated with Python

[✓] SQL validation script created

[✓] Task requirements completed


============================================================
22. FINAL STATUS
============================================================

TASK 1 STATUS: COMPLETED


The Olist dataset is now available in a local PostgreSQL database
running through Docker.

The database can be queried successfully, the main table
relationships have been tested and validated, and the future machine
learning problem has been understood.

The project is ready for the next MLOps training task.


============================================================
END OF TASK 1 DOCUMENTATION
============================================================
