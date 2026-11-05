
from brain import TinyLocalAI

def main():
    bot = TinyLocalAI()
    print("\nTinyLocalAI — offline mini assistant")
    print("No internet or heavy AI libraries required.")
    print("Commands: /help, /teach, /list, /forget, /quit\n")

    while True:
        try:
            message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAI: Bye!")
            break

        if not message:
            continue
        command = message.lower()

        if command in ("/quit", "/exit"):
            print("AI: Bye!")
            break
        elif command == "/help":
            print(bot.help_text())
            continue
        elif command == "/teach":
            question = input("Question: ").strip()
            answer = input("Answer: ").strip()
            if question and answer:
                bot.teach(question, answer)
                print("AI: Learned that Q&A pair and saved it.")
            else:
                print("AI: Both fields are needed.")
            continue
        elif command == "/list":
            for i, item in enumerate(bot.knowledge, 1):
                print(f"{i}. {item['question']} -> {item['answer']}")
            continue
        elif command == "/forget":
            query = input("Question to remove (exact or close wording): ").strip()
            removed = bot.forget(query)
            print("AI: Removed." if removed else "AI: Couldn't find a close match.")
            continue

        answer, score = bot.reply(message)
        print(f"AI: {answer}")

if __name__ == "__main__":
    main()
