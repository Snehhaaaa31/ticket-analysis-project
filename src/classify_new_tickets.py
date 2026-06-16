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

    tickets_df = pd.read_csv(
        "data/tickets.csv"
    )

    classified_df = pd.read_csv(
        "output/classified_tickets_batch.csv"
    )

    new_tickets = tickets_df[
        ~tickets_df["ticket_id"].isin(
            classified_df["ticket_id"]
        )
    ]

    print(
        f"New tickets found: {len(new_tickets)}"
    )

    if len(new_tickets) == 0:
        print("No new tickets to classify.")
        return

    tickets = new_tickets.to_dict(
        "records"
    )

    results = []

    total_batches = (
        len(tickets) + BATCH_SIZE - 1
    ) // BATCH_SIZE

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

            print(
                f"FAILED: {e}"
            )

    if len(results) > 0:

        results_df = pd.DataFrame(
            results
        )

        updated_df = pd.concat(
            [
                classified_df,
                results_df
            ],
            ignore_index=True
        )

        updated_df.to_csv(
            "output/classified_tickets_batch.csv",
            index=False
        )

        print(
            f"\nAdded "
            f"{len(results_df)} "
            f"new classified tickets."
        )

        print(
            f"Total classified tickets: "
            f"{len(updated_df)}"
        )


if __name__ == "__main__":
    main()