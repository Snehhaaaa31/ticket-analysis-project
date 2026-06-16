import os
import json
import re
from datetime import datetime

import pandas as pd
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_ticket(ticket_text):
    prompt = f"""
You are a customer support analyst.

Classify the ticket into one of these categories:
Authentication, Billing, Delivery, Technical, General Inquiry.

Return only JSON.

Ticket:
{ticket_text}

Format:
{{
    "category": "",
    "priority": "",
    "sentiment": "",
    "summary": ""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    content = re.sub(
        r"```json|```",
        "",
        content
    ).strip()

    return json.loads(content)


def main():

    tickets = pd.read_csv("data/tickets.csv")

    results = []
    failed = []

    for _, row in tickets.iterrows():

        ticket_id = row["ticket_id"]
        ticket_text = row["ticket_text"]

        print(f"Processing ticket {ticket_id}")

        try:

            result = classify_ticket(ticket_text)

            results.append({
                "ticket_id": ticket_id,
                "ticket_text": ticket_text,
                "category": result.get("category"),
                "priority": result.get("priority"),
                "sentiment": result.get("sentiment"),
                "summary": result.get("summary"),
                "processed_at": datetime.now()
            })

        except Exception as e:

            failed.append({
                "ticket_id": ticket_id,
                "ticket_text": ticket_text,
                "error": str(e),
                "processed_at": datetime.now()
            })

    pd.DataFrame(results).to_csv(
        "output/classified_tickets.csv",
        index=False
    )

    pd.DataFrame(failed).to_csv(
        "output/failed_tickets.csv",
        index=False
    )

    print(f"\nProcessed: {len(results)}")
    print(f"Failed: {len(failed)}")


if __name__ == "__main__":
    main()
    