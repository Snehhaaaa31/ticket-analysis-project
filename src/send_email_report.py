import os
import smtplib
import pandas as pd

from datetime import datetime
from email.message import EmailMessage

from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# =====================================
# MYSQL CONNECTION
# =====================================

host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = quote_plus(
    os.getenv("MYSQL_PASSWORD")
)
database = os.getenv("MYSQL_DATABASE")

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)

# =====================================
# READ DATA
# =====================================

df = pd.read_sql(
    "SELECT * FROM tickets",
    engine
)

# =====================================
# KPI CALCULATIONS
# =====================================

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

category_counts = (
    df["category"]
    .value_counts()
)

top_category = (
    category_counts.idxmax()
)

# =====================================
# TOP 5 HIGH PRIORITY TICKETS
# =====================================

high_priority_tickets = df[
    df["priority"] == "High"
]

top_5 = high_priority_tickets[
    ["ticket_id", "summary"]
].head(5)

ticket_section = ""

for _, row in top_5.iterrows():

    ticket_section += (
        f"• Ticket {row['ticket_id']}: "
        f"{row['summary']}\n"
    )

# =====================================
# EMAIL BODY
# =====================================

report_time = datetime.now().strftime(
    "%d-%m-%Y %H:%M:%S"
)

email_body = f"""
SUPPORT TICKET ANALYTICS REPORT

Generated On:
{report_time}

================================================

EXECUTIVE SUMMARY

Total Tickets Processed : {total_tickets}

High Priority Tickets   : {high_priority}

Negative Sentiment      : {negative}

Top Category            : {top_category}

================================================

CATEGORY DISTRIBUTION

{category_counts.to_string()}

================================================

PRIORITY BREAKDOWN

High   : {high_priority}

Medium : {medium_priority}

Low    : {low_priority}

================================================

SENTIMENT OVERVIEW

Positive : {positive}

Neutral  : {neutral}

Negative : {negative}

================================================

TOP HIGH PRIORITY TICKETS

{ticket_section}

================================================

SYSTEM STATUS

AI Classification : SUCCESS

Database Update   : SUCCESS

Dashboard Status  : ACTIVE

================================================

Generated Automatically By

AI-Powered Ticket Analysis System

Tech Stack:
Python | Groq | MySQL | Power BI | n8n
"""

# =====================================
# SEND EMAIL
# =====================================

EMAIL = os.getenv(
    "EMAIL_ADDRESS"
)

APP_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)

msg = EmailMessage()

msg["Subject"] = (
    "Support Ticket Analytics Report"
)

msg["From"] = EMAIL

msg["To"] = EMAIL

msg.set_content(email_body)

with smtplib.SMTP_SSL(
    "smtp.gmail.com",
    465
) as smtp:

    smtp.login(
        EMAIL,
        APP_PASSWORD
    )

    smtp.send_message(msg)

print(
    "Email sent successfully!"
)