import pandas as pd

SHEET_ID = "1GciFl9jA1D6lOaRHKUThGxLlD6dqkgT6InqtW5jApsU"

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"


# Existing tickets
existing_df = pd.read_csv("data/tickets.csv")

# Google Form responses
google_df = pd.read_csv(url)

# Get ticket descriptions
new_tickets = google_df[["Ticket Description"]]
new_tickets.columns = ["ticket_text"]

# Remove duplicates
existing_texts = set(
    existing_df["ticket_text"].str.strip().str.lower()
)

new_tickets = new_tickets[
    ~new_tickets["ticket_text"]
    .str.strip()
    .str.lower()
    .isin(existing_texts)
]

# Create new ticket IDs
start_id = existing_df["ticket_id"].max() + 1

new_tickets.insert(
    0,
    "ticket_id",
    range(start_id, start_id + len(new_tickets))
)

# Append
updated_df = pd.concat(
    [existing_df, new_tickets],
    ignore_index=True
)

# Save
updated_df.to_csv(
    "data/tickets.csv",
    index=False
)

print(
    f"Added {len(new_tickets)} new tickets."
)

print(
    f"Total tickets now: {len(updated_df)}"
)