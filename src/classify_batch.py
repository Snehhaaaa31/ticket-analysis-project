import os
import json
import re
from datetime import datetime

import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

BATCH_SIZE = 20


def classify_batch(batch):

    batch_text = ""

    for item in batch:
        batch_text += (
            f"{item['ticket_id']}. "
            f"{item['ticket_text']}\n"
        )

    prompt = f"""
You are a customer support analyst.

Classify each ticket into one of these categories:

- Authentication
- Billing
- Delivery
- Technical
- General Inquiry

Priority:
- High
- Medium
- Low

Sentiment:
- Positive
- Neutral
- Negative

Return ONLY a JSON array.

Tickets:

{batch_text}

Return format:

[
    {{
        "ticket_id": 1,
        "ticket_text": "",
        "category": "",
        "priority": "",
        "sentiment": "",
        "summary": ""
    }}
]
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

    df = pd.read_csv("data/tickets.csv")

    tickets = df.to_dict("records")

    results = []
    failed_batches = []

    total_batches = (
        len(tickets) + BATCH_SIZE - 1
    ) // BATCH_SIZE

    print(f"\nTotal Tickets: {len(tickets)}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Total Batches: {total_batches}\n")

    for i in range(
        0,
        len(tickets),
        BATCH_SIZE
    ):

        batch_number = (
            i // BATCH_SIZE
        ) + 1

        batch = tickets[
            i:i + BATCH_SIZE
        ]

        print(
            f"Processing Batch "
            f"{batch_number}/{total_batches}"
        )

        try:

            batch_results = classify_batch(
                batch
            )

            for item in batch_results:

                item["processed_at"] = (
                    datetime.now()
                )

            results.extend(
                batch_results
            )

            print("SUCCESS")

        except Exception as e:

            print("FAILED")

            failed_batches.append({
                "batch_number": batch_number,
                "error": str(e)
            })

    output_df = pd.DataFrame(results)

    output_df.to_csv(
        "output/classified_tickets_batch.csv",
        index=False
    )

    failed_df = pd.DataFrame(
        failed_batches
    )

    failed_df.to_csv(
        "output/failed_batches.csv",
        index=False
    )

    print("\n==========")
    print("COMPLETE")
    print("==========")
    print(
        f"Processed: {len(results)}"
    )
    print(
        f"Failed Batches: {len(failed_batches)}"
    )


if __name__ == "__main__":
    main()