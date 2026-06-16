import pandas as pd
import random

authentication = [
    "Unable to login after password reset",
    "Forgot password and cannot access account",
    "Account locked after multiple login attempts",
    "Two-factor authentication code not working",
    "Login page keeps showing invalid credentials"
]

billing = [
    "Payment deducted twice from my account",
    "Invoice amount is incorrect",
    "Refund has not been received",
    "Subscription renewed without notice",
    "Charged for a cancelled order"
]

delivery = [
    "Order not delivered after 10 days",
    "Package marked delivered but not received",
    "Tracking number is not updating",
    "Delivery delayed without notification",
    "Wrong item delivered"
]

technical = [
    "Website is loading very slowly",
    "Application crashes on startup",
    "Unable to upload documents",
    "Error message appears during checkout",
    "Search functionality not working"
]

general = [
    "Need information about premium plan",
    "How can I update my profile details",
    "Where can I download my invoice",
    "What are your support hours",
    "How do I change notification settings"
]

tickets = []

all_categories = (
    authentication +
    billing +
    delivery +
    technical +
    general
)

for i in range(1, 201):

    ticket = random.choice(all_categories)

    tickets.append({
        "ticket_id": i,
        "ticket_text": ticket
    })

df = pd.DataFrame(tickets)

df.to_csv(
    "data/tickets.csv",
    index=False
)

print("200 tickets generated successfully.")