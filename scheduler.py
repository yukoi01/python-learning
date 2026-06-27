import schedule
import time
import pandas as pd
from groq import Groq
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_expense_report():
    print("Running expense report...")

    # Load and analyze
    df = pd.read_csv("my_expenses.csv")
    total = df["amount"].sum()
    biggest = df.sort_values("amount", ascending=False).iloc[0]
    category_totals = df.groupby("category")["amount"].sum()

    # Get AI analysis
    client = Groq(api_key="your_groq_key_here")
    prompt = f"""
    Total spent: {total}
    Biggest expense: {biggest['item']} costing {biggest['amount']}
    Category breakdown: {category_totals.to_string()}
    Give me 3 short money saving tips.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a personal finance advisor. Be concise."},
            {"role": "user", "content": prompt}
        ]
    )
    ai_analysis = response.choices[0].message.content

    # Send email
    sender = "snehasama7@gmail.com"
    receiver = "snehasama7@gmail.com"
    password = "your_app_password_here"

    body = f"""
Hi Koi!

📊 EXPENSE SUMMARY
Total Spent: {total}
Biggest Expense: {biggest['item']} - {biggest['amount']}

📂 BY CATEGORY
{category_totals.to_string()}

🤖 AI TIPS
{ai_analysis}

Sent automatically by Python 🐍
"""
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Your Automated Expense Report 📊"
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("Report sent!")
    except Exception as e:
        print(f"Error: {e}")

# Schedule it
schedule.every(1).minutes.do(send_expense_report)

print("Scheduler running! Report will send every minute.")

while True:
    schedule.run_pending()
    time.sleep(1)