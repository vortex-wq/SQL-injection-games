#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 8 (Defender Mode: Fix the Vulnerabilities)

Final epilogue level:
You switch roles from attacker to defender and choose the correct
secure coding patterns to prevent SQL injection.
"""

import textwrap


def print_wrapped(text: str) -> None:
    print(textwrap.dedent(text).strip())
    print()


QUESTIONS = [
    {
        "title": "Login query in Python",
        "description": """
        You see this Python code using a raw SQL string:

            user = request.form["username"]
            pwd = request.form["password"]

            query = "SELECT * FROM users WHERE username='" + user + \
                    "' AND password='" + pwd + "';"

            cursor.execute(query)

        How should this be fixed?
        """,
        "options": {
            "A": 'Escape quotes in user and pwd manually before concatenation.',
            "B": 'Use parameterized queries with placeholders, e.g. cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd)).',
            "C": 'Base64-encode user and pwd before concatenation.',
            "D": 'Strip any occurrence of " OR " from user and pwd.',
        },
        "correct": "B",
        "explanation": """
        The only robust fix here is to use parameterized queries so that user and
        pwd are always treated as data, never as SQL code.

        Manual escaping, base64-encoding or blacklisting pieces like " OR "
        are all bypassable and not considered safe defenses.

        Prepared/parameterized statements are the standard defense.
        """
    },
    {
        "title": "Search feature with LIKE",
        "description": """
        A search feature uses this pseudo-code:

            term = request.GET["q"]
            sql = "SELECT id, title FROM posts WHERE title LIKE '%" + term + "%';"
            db.query(sql)

        What is the BEST way to secure this?
        """,
        "options": {
            "A": 'Replace any "%" or "_" from term, then concatenate.',
            "B": 'Use parameterized queries and pass the pattern as a parameter, e.g. "... WHERE title LIKE ?" with "%" + term + "%".',
            "C": 'HTML-encode term before putting it into SQL.',
            "D": 'This is safe because LIKE will not execute injected SQL.',
        },
        "correct": "B",
        "explanation": """
        The right approach is still to use parameterized queries and pass
        the whole LIKE pattern as a bound parameter.

        Removing %, HTML-encoding, or assuming LIKE is safe are all wrong:
        the core problem is direct string concatenation into SQL.
        """
    },
    {
        "title": "Least-privilege database account",
        "description": """
        Your web app connects to the database using a user 'webapp' that has:

          - SELECT, INSERT, UPDATE, DELETE on *all* tables
          - ALTER, DROP on *all* tables
          - SUPER / admin-like privileges

        How should you change this to reduce SQL injection impact?
        """,
        "options": {
            "A": 'No change needed; app needs full power in case of future features.',
            "B": 'Give the webapp user only the minimal privileges it needs on specific tables.',
            "C": 'Use the root DB account but hide the password carefully.',
            "D": 'Rotate the root password weekly but keep privileges the same.',
        },
        "correct": "B",
        "explanation": """
        Even if an injection occurs, least-privilege design limits the damage.

        The webapp DB user should have only the minimal permissions needed
        (e.g., maybe SELECT/INSERT on a few tables, not DROP/ALTER everywhere).

        Root-style accounts from the app are a big design flaw.
        """
    },
    {
        "title": "Error messages and information leakage",
        "description": """
        When SQL errors happen, the app shows full DB error messages in the browser:

            SQLSTATE[42000]: Syntax error or access violation: 1064
            You have an error in your SQL syntax near ...

        Why is this a problem in the context of SQL injection?
        """,
        "options": {
            "A": "It lets attackers learn about the underlying query structure and DB engine, helping craft better payloads.",
            "B": "It slows down the page load time.",
            "C": "It uses extra disk space on the server.",
            "D": "It is not a problem; detailed errors are always good.",
        },
        "correct": "A",
        "explanation": """
        Detailed SQL errors reveal query structure, table/column names,
        DB version and engine. Attackers can use these hints to refine
        their SQL injection payloads.

        Apps should log the details internally but show only generic messages
        to end users.
        """
    },
    {
        "title": "Client-side validation vs server-side validation",
        "description": """
        A developer adds JavaScript validation in the browser to block
        characters like ' or " from an input field, hoping it will prevent SQLi.

        Is this enough?
        """,
        "options": {
            "A": "Yes, because users cannot bypass JavaScript.",
            "B": "No, because attackers can send requests directly to the server and skip client-side checks.",
            "C": "Yes, as long as combined with a CAPTCHA.",
            "D": "Yes, for mobile clients only.",
        },
        "correct": "B",
        "explanation": """
        Client-side validation is easily bypassed: attackers can disable JS,
        modify requests, or use tools like curl/Burp.

        Server-side validation and parameterized queries are still required,
        regardless of front-end checks.
        """
    },
]


def ask_question(q):
    print("=" * 70)
    print(f"Question: {q['title']}")
    print("=" * 70)
    print_wrapped(q["description"])
    print("Options:")
    for key, text in q["options"].items():
        print(f"  {key}) {text}")
    print()

    while True:
        answer = input("Your answer (A/B/C/D, or 'hint'): ").strip().upper()
        if answer == "HINT":
            print_wrapped("Hint: Think about parameterized queries, least privilege, and not trusting the client.")
            continue
        if answer in q["options"]:
            return answer
        print("Please enter A, B, C, or D (or 'hint').")


def level_8():
    print("=" * 70)
    print("LEVEL 8: Defender Mode - Fix the SQL Injection")
    print("=" * 70)

    intro = """
    In all previous levels you played the ATTACKER.

    In this final level, you switch roles:
      You are the BACKEND DEVELOPER who must DEFEND the app.

    You'll see several scenarios with vulnerable code or design,
    and you must choose the BEST way to fix or mitigate SQL injection.
    """
    print_wrapped(intro)

    score = 0

    for q in QUESTIONS:
        ans = ask_question(q)
        if ans == q["correct"]:
            print("\n✅ Correct!")
            score += 1
        else:
            print(f"\n❌ Incorrect. The correct answer is {q['correct']}.")

        print_wrapped("\nExplanation:\n" + q["explanation"])
        input("Press Enter to continue to the next question...")

    print("=" * 70)
    print("Level 8 Results")
    print("=" * 70)
    print(f"You answered {score} out of {len(QUESTIONS)} correctly.")

    if score == len(QUESTIONS):
        print("🎉 Perfect! You understand both attacking AND defending against SQLi.")
    elif score >= len(QUESTIONS) - 1:
        print("🔥 Great job! Just a tiny bit more polishing and you're solid.")
    else:
        print("🧠 Not bad. Review the explanations and try again to strengthen your defender mindset.")

    outro = """
    Takeaway:

      - Knowing how to exploit SQL injection is powerful.
      - Knowing how to PREVENT it is what makes you a good engineer
        and security-conscious developer.

    Core defenses to remember:

      1) Always use parameterized / prepared statements.
      2) Never concatenate raw user input into SQL strings.
      3) Apply least-privilege on database accounts.
      4) Avoid leaking detailed errors to users.
      5) Validate and sanitize inputs on the server-side.

    Congrats on completing the SQL Injection Adventure series!
    """
    print_wrapped(outro)
    return True


def main():
    print("=" * 70)
    print("   SQL Injection Adventure - Level 8: Defender Mode")
    print("=" * 70)

    disclaimer = """
    This level focuses on SECURE coding practices.

    Remember:
      A great security engineer understands both how attacks work
      AND how to build systems that are hard to attack.
    """
    print_wrapped(disclaimer)

    level_8()

    print("=" * 70)
    print("GAME OVER - YOU FINISHED ALL 8 LEVELS 🎉")
    print("=" * 70)


if __name__ == "__main__":
    main()
