import schedule
import time
import pandas as pd
from groq import Groq
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

send_count = 0
max_sends = 8  # 8 mondays = 2 months

def send_expense_report():
    global send_count
    send_count += 1
    print(f"Sending report {send_count} of {max_sends}...")

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

Report {send_count} of {max_sends}
Sent automatically by Python 🐍
"""
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = f"Weekly Expense Report ({send_count}/{max_sends}) 📊"
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print(f"Report {send_count} sent!")
    except Exception as e:
        print(f"Error: {e}")

    if send_count >= max_sends:
        print("2 months done! Stopping scheduler.")
        schedule.cancel_job(job)

# Change to every().monday.at("09:00") for real use
job = schedule.every(1).minutes.do(send_expense_report)

print("Scheduler running!")

while True:
    schedule.run_pending()
    time.sleep(1)