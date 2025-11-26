from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Rule:
    """Represents a simple rule with a regex pattern and canned reply."""

    pattern: re.Pattern[str]
    reply: str


class RuleBasedChatbot:
    """Minimal chatbot that matches user messages against regex rules."""

    def __init__(self) -> None:
        self._rules = self._build_rules()

    def _build_rules(self) -> list[Rule]:
        """Compile regex patterns once so matching stays fast."""
        rule_specs = [
            (r"\bhello\b|\bhi\b|\bhey\b", "Hello! How can I help you today?"),
            (r"\bhow (are|r) (you|u)\b", "I'm just code, but I'm doing great!"),
            (r"\b(weather|temperature)\b", "I can't check weather yet, but you can try a weather app."),
            (r"\bname\b", "I'm a tiny rule-based bot written in Python."),
            (r"\b(help|support)\b", "Sure—describe the issue and I'll try to help."),
            (r"\b(thank(s)?|thx)\b", "You're welcome!"),
            (r"\b(bye|goodbye|see you)\b", "Goodbye! Talk soon."),
        ]
        return [Rule(re.compile(pattern, re.IGNORECASE), reply) for pattern, reply in rule_specs]

    def get_response(self, message: str) -> str:
        """Return the first matching rule response or a fallback."""
        cleaned = message.strip()
        if not cleaned:
            return "Say something so I can respond 🙂"

        for rule in self._rules:
            if rule.pattern.search(cleaned):
                return rule.reply
        return "I don't understand yet, but I'm learning!"

    def chat(self) -> None:
        """Simple REPL loop."""
        print("RuleBot: Hello! Type 'quit' to exit.")
        while True:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                print("\nRuleBot: Bye!")
                break

            if user_input.strip().lower() in {"quit", "exit"}:
                print("RuleBot: Bye!")
                break

            response = self.get_response(user_input)
            print(f"RuleBot: {response}")


if __name__ == "__main__":
    bot = RuleBasedChatbot()
    bot.chat()

