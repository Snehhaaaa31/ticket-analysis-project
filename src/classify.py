import os
import json
import re


from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

ticket = "Unable to login after password reset"

prompt = f"""
Classify this support ticket.

Return ONLY valid JSON.

Ticket:
{ticket}

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

raw_response = response.choices[0].message.content

clean_json = re.sub(r"```json|```", "", raw_response).strip()

result = json.loads(clean_json)

print(result)