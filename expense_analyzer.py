import pandas as pd
from groq import Groq

# Load the data
df = pd.read_csv("my_expenses.csv")

# Calculate stats
total = df["amount"].sum()
biggest = df.sort_values("amount", ascending=False).iloc[0]
category_totals = df.groupby("category")["amount"].sum()

print(f"Total spent: {total}")
print(f"Biggest expense: {biggest['item']} - {biggest['amount']}")
print(category_totals)
client = Groq(api_key="your_api_key_here")

prompt = f"""
Here are my expenses:
- Total spent: {total}
- Biggest expense: {biggest['item']} costing {biggest['amount']}
- Category breakdown:
{category_totals.to_string()}

Please analyze my spending and give me 3 specific money saving tips based on this data.
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a personal finance advisor. Be specific, practical and concise."},
        {"role": "user", "content": prompt}
    ]
)

print("\n--- AI Analysis ---")
print(response.choices[0].message.content)