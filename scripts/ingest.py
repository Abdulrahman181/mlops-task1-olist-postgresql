import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import Text, BigInteger, Float, DateTime


DATABASE_URL = (
    "postgresql+psycopg2://"
    "olist_user:olist_password@localhost:5432/olist_db"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "archive")

TABLE_MAP = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category_translation",
}

TEXT_COLUMNS = {
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state",
    "geolocation_city",
    "geolocation_state",
    "order_id",
    "product_id",
    "seller_id",
    "order_status",
    "payment_type",
    "review_id",
    "review_comment_title",
    "review_comment_message",
    "product_category_name",
    "product_category_name_english",
}

INTEGER_COLUMNS = {
    "customer_zip_code_prefix",
    "geolocation_zip_code_prefix",
    "order_item_id",
    "payment_sequential",
    "payment_installments",
    "review_score",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
}

FLOAT_COLUMNS = {
    "geolocation_lat",
    "geolocation_lng",
    "price",
    "freight_value",
    "payment_value",
}

DATETIME_COLUMNS = {
    "shipping_limit_date",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "review_creation_date",
    "review_answer_timestamp",
}


def prepare_dataframe(df):
    for column in df.columns:
        if column in DATETIME_COLUMNS:
            df[column] = pd.to_datetime(df[column], errors="coerce")

        elif column in INTEGER_COLUMNS:
            df[column] = pd.to_numeric(df[column], errors="coerce")

        elif column in FLOAT_COLUMNS:
            df[column] = pd.to_numeric(df[column], errors="coerce")

        elif column in TEXT_COLUMNS:
            df[column] = df[column].astype("string")

    return df


def get_sql_types(columns):
    dtype = {}

    for column in columns:
        if column in DATETIME_COLUMNS:
            dtype[column] = DateTime()
        elif column in INTEGER_COLUMNS:
            dtype[column] = BigInteger()
        elif column in FLOAT_COLUMNS:
            dtype[column] = Float()
        else:
            dtype[column] = Text()

    return dtype


def validate_source_files():
    missing = []

    for filename in TABLE_MAP:
        path = os.path.join(CSV_DIR, filename)

        if not os.path.isfile(path):
            missing.append(filename)

    if missing:
        raise FileNotFoundError(
            "Missing CSV files:\n" + "\n".join(missing)
        )


def test_connection(engine):
    with engine.connect() as connection:
        version = connection.execute(text("SELECT version();")).scalar()

    print("Database connection successful:")
    print(version)
    print()


def load_table(engine, filename, table_name):
    file_path = os.path.join(CSV_DIR, filename)

    print("=" * 60)
    print(f"Loading: {filename}")
    print(f"Target table: {table_name}")

    df = pd.read_csv(file_path, low_memory=False)

    print(f"Rows read: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    df = prepare_dataframe(df)
    dtype = get_sql_types(df.columns)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        dtype=dtype,
        chunksize=5000,
        method="multi",
    )

    with engine.connect() as connection:
        count = connection.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar()

    if count != len(df):
        raise RuntimeError(
            f"Row count mismatch for {table_name}: "
            f"CSV={len(df):,}, DB={count:,}"
        )

    print(f"Rows in database: {count:,}")
    print("Done.")


def main():
    print("=" * 60)
    print("Olist Dataset -> PostgreSQL Ingestion")
    print("=" * 60)
    print(f"Project directory: {BASE_DIR}")
    print(f"CSV directory:     {CSV_DIR}")
    print()

    validate_source_files()

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )

    test_connection(engine)

    for filename, table_name in TABLE_MAP.items():
        load_table(engine, filename, table_name)

    print()
    print("=" * 60)
    print("All tables loaded successfully.")
    print("=" * 60)

    engine.dispose()


if __name__ == "__main__":
    main()