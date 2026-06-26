import pandas as pd
from groq import Groq
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---- CONFIG ----
sender = "snehasama7@gmail.com"
receiver = "snehasama7@gmail.com"
email_password = "your_app_password_here"
groq_api_key = "your_groq_key_here"

# ---- STEP 1: Load and analyze expenses ----
df = pd.read_csv("my_expenses.csv")

total = df["amount"].sum()
biggest = df.sort_values("amount", ascending=False).iloc[0]
category_totals = df.groupby("category")["amount"].sum()

# ---- STEP 2: Get AI analysis ----
client = Groq(api_key=groq_api_key)

prompt = f"""
Here are my expenses:
- Total spent: {total}
- Biggest expense: {biggest['item']} costing {biggest['amount']}
- Category breakdown:
{category_totals.to_string()}

Give me a short 3 tip money saving analysis based on this data.
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a personal finance advisor. Be specific and concise."},
        {"role": "user", "content": prompt}
    ]
)

ai_analysis = response.choices[0].message.content

# ---- STEP 3: Build the email ----
subject = "Your Weekly Expense Report 📊"

body = f"""
Hi Koi!

Here is your automated expense report:

📊 EXPENSE SUMMARY
------------------
Total Spent: {total}
Biggest Expense: {biggest['item']} - {biggest['amount']}

📂 BY CATEGORY
--------------
{category_totals.to_string()}

🤖 AI FINANCIAL TIPS
--------------------
{ai_analysis}

---
Sent automatically by your Python script 🐍
"""

# ---- STEP 4: Send the email ----
try:
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, email_password)
    server.send_message(msg)
    server.quit()

    print("Expense report sent to your email!")

except Exception as e:
    print(f"Something went wrong: {e}")