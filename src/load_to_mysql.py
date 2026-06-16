import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = quote_plus(
    os.getenv("MYSQL_PASSWORD")
)
database = os.getenv("MYSQL_DATABASE")

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)

# CSV data
csv_df = pd.read_csv(
    "output/classified_tickets_batch.csv"
)

# Existing MySQL data
sql_df = pd.read_sql(
    "SELECT ticket_id FROM tickets",
    engine
)

# Find only new tickets
new_df = csv_df[
    ~csv_df["ticket_id"].isin(
        sql_df["ticket_id"]
    )
]

print(
    f"New records found: {len(new_df)}"
)

if len(new_df) > 0:

    new_df.to_sql(
        "tickets",
        con=engine,
        if_exists="append",
        index=False
    )

    print(
        f"{len(new_df)} records loaded successfully."
    )

else:

    print(
        "No new records to load."
    )