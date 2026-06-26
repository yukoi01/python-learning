from groq import Groq

client = Groq(api_key="your_api_key_here")

conversation_history = []

conversation_history = [
    {"role": "system", "content": "admin "}
]

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
        break

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history
    )

    ai_reply = response.choices[0].message.content
    conversation_history.append({"role": "system", "content": ai_reply})

    print(f"\nAI: {ai_reply}")