import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = quote_plus(os.getenv("MYSQL_PASSWORD"))
database = os.getenv("MYSQL_DATABASE")

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)

df = pd.read_csv("output/classified_tickets_batch.csv")

df.to_sql(
    "tickets",
    con=engine,
    if_exists="append",
    index=False
)

print(f"{len(df)} records loaded successfully.")