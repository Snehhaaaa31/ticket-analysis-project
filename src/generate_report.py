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

# Read MySQL table
df = pd.read_sql(
    "SELECT * FROM tickets",
    engine
)

# KPIs
total_tickets = len(df)

high_priority = len(
    df[df["priority"] == "High"]
)

medium_priority = len(
    df[df["priority"] == "Medium"]
)

low_priority = len(
    df[df["priority"] == "Low"]
)

positive = len(
    df[df["sentiment"] == "Positive"]
)

neutral = len(
    df[df["sentiment"] == "Neutral"]
)

negative = len(
    df[df["sentiment"] == "Negative"]
)

top_category = (
    df["category"]
    .value_counts()
    .idxmax()
)

print("\n===== REPORT =====")

print(f"Total Tickets: {total_tickets}")
print(f"High Priority: {high_priority}")
print(f"Medium Priority: {medium_priority}")
print(f"Low Priority: {low_priority}")

print(f"Positive: {positive}")
print(f"Neutral: {neutral}")
print(f"Negative: {negative}")

print(f"Top Category: {top_category}")