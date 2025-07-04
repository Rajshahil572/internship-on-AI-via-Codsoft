# Simple Chatbot with Rule-Based Responses

print("Welcome to SimpleChat! Type 'bye' to exit.\n")

while True:
    user_input = input("You: ").lower().strip()

    # Exit condition
    if user_input == "bye":
        print("Chatbot: Goodbye! Have a great day.")
        break

    # Greetings
    elif user_input in ["hi", "hello", "hey"]:
        print("Chatbot: Hello! How can I help you?")

    # Asking about well-being
    elif "how are you" in user_input:
        print("Chatbot: I'm just a chatbot, but I'm doing fine! Thanks for asking.")

    # Asking for the chatbot's name
    elif "your name" in user_input:
        print("Chatbot: I'm SimpleChat, your friendly assistant.")

    # Help request
    elif "help" in user_input:
        print("Chatbot: Sure, I can help. Ask me about my features or say 'bye' to exit.")

    # Time inquiry
    elif "time" in user_input:
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        print(f"Chatbot: The current time is {current_time}.")

    # Date inquiry
    elif "date" in user_input:
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        print(f"Chatbot: Today's date is {current_date}.")

    # Default response
    else:
        print("Chatbot: Sorry, I didn't understand that. Can you rephrase?")
