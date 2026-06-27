"""
Smart Personal Assistant Agent — Agentic AI Mini Project
----------------------------------------------------------
This program demonstrates a simple AGENT that follows the classic
agentic loop: PERCEIVE -> DECIDE -> ACT -> RESPOND.

It has 4 "tools" it can autonomously choose between based on what
the user types, instead of running one fixed task:
  1. Calculator
  2. Date & Time lookup
  3. To-Do list manager
  4. Wikipedia search

Run it and just chat with it naturally.
"""

import datetime
import re

# ---------- Memory (agent's internal state) ----------
todo_list = []

# ---------- TOOLS the agent can use ----------

def calculator(expression):
    """Tool 1: Solve a basic math expression."""
    try:
        allowed = set("0123456789+-*/(). ")
        if not set(expression) <= allowed or expression.strip() == "":
            return "Sorry, I can only do basic math like + - * /."
        return f"Result: {eval(expression)}"
    except Exception:
        return "Sorry, I couldn't calculate that."


def get_datetime():
    """Tool 2: Return current date and time."""
    now = datetime.datetime.now()
    return f"Current date & time: {now.strftime('%A, %d %B %Y, %I:%M %p')}"


def add_task(task):
    """Tool 3a: Add an item to the to-do list."""
    task = task.strip()
    if not task:
        return "Please tell me what task to add."
    todo_list.append(task)
    return f"Added to your to-do list: '{task}'"


def view_tasks():
    """Tool 3b: Show the to-do list."""
    if not todo_list:
        return "Your to-do list is empty."
    return "Your tasks:\n" + "\n".join(f"{i+1}. {t}" for i, t in enumerate(todo_list))


def search_wikipedia(query):
    """Tool 4: Look up a topic on Wikipedia."""
    query = query.strip()
    if not query:
        return "Please tell me what to search for."
    try:
        import wikipedia
        try:
            return wikipedia.summary(query, sentences=2, auto_suggest=True)
        except wikipedia.exceptions.DisambiguationError as e:
            # Multiple matches found -> just use the first suggested option
            return wikipedia.summary(e.options[0], sentences=2, auto_suggest=False)
        except wikipedia.exceptions.PageError:
            # No exact page -> fall back to a manual search first
            results = wikipedia.search(query)
            if results:
                return wikipedia.summary(results[0], sentences=2, auto_suggest=False)
            return f"Sorry, I couldn't find a Wikipedia page for '{query}'."
    except Exception:
        return "Sorry, couldn't find info on that (check your internet connection)."


# ---------- DECISION ENGINE (the "brain" of the agent) ----------

def decide_action(user_input):
    """
    This is the agent's reasoning step: it looks at what the user said
    and decides which tool is the right one to call. This is what makes
    it an AGENT rather than a single-purpose script.
    """
    text = user_input.lower()

    if "add task" in text or "remind me to" in text:
        key = "add task" if "add task" in text else "remind me to"
        return add_task(text.split(key, 1)[-1])

    elif "show task" in text or "my task" in text or "todo" in text or "to-do" in text:
        return view_tasks()

    elif any(op in text for op in ["+", "-", "*", "/", "calculate", "calc"]):
        expr = re.sub(r"[^0-9+\-*/(). ]", "", text)
        return calculator(expr)

    elif "time" in text or "date" in text:
        return get_datetime()

    elif "who is" in text or "what is" in text or "search" in text:
        topic = text.replace("who is", "").replace("what is", "").replace("search", "")
        return search_wikipedia(topic)

    else:
        return ("I'm not sure how to help with that yet. Try things like:\n"
                "  'what is the time'\n  'calculate 12*8'\n"
                "  'add task buy milk'\n  'show tasks'\n  'who is Alan Turing'")


# ---------- AGENT LOOP ----------

def run_agent():
    print("Agent: Hi! I'm your personal assistant agent.")
    print("Try: 'what is the time', 'calculate 5*7', 'add task buy milk',")
    print("     'show tasks', 'who is Alan Turing'")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower().strip() == "exit":
            print("Agent: Goodbye!")
            break
        response = decide_action(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    run_agent()
