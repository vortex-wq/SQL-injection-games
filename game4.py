#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 4 (Blind SQL Injection - Boolean-based)

Educational project to understand blind SQL injection where you only see
TRUE/FALSE behaviour (login success or failure), not the actual SQL errors
or returned data.
"""

import textwrap


def print_wrapped(text: str) -> None:
    print(textwrap.dedent(text).strip())
    print()


def level_4():
    print("=" * 70)
    print("LEVEL 4: Blind SQL Injection (Boolean-based)")
    print("=" * 70)

    description = """
    Scenario:

    You are attacking a login form for a user 'admin'.

    The backend runs this query:

        SELECT * FROM users
        WHERE username = 'admin'
          AND password = '<USER_INPUT>';

    Important:
      - You do NOT see SQL errors.
      - You do NOT see query results.
      - You only see:
          - "Welcome back, admin!"   (if condition is TRUE)
          - "Invalid login."         (if condition is FALSE)

    This is a classic case of BLIND SQL injection:
      You infer what's happening from TRUE/FALSE behaviour only.

    Goal:
      Craft a password payload that makes the condition always TRUE,
      even though you don't know the real admin password.

    Hint:
      Think about the login-bypass payload from Level 1:
        ' OR '1'='1
    """

    print_wrapped(description)

    max_attempts = 6
    attempts = 0

    while attempts < max_attempts:
        password = input("Enter password for admin (or 'hint' / 'quit'): ").strip()

        if password.lower() == "quit":
            print("\nExiting game. Goodbye!")
            exit(0)

        if password.lower() == "hint":
            print_wrapped("""
            Hint:
              - The query is:

                    SELECT * FROM users
                    WHERE username = 'admin'
                      AND password = '<USER_INPUT>';

              - You want to turn the password condition into something that is
                always TRUE.

              - Try payloads like:
                    ' OR '1'='1
                    ' OR 1=1--
            """)
            continue

        attempts += 1

        normalized = password.lower().replace('"', "'").strip()

        # Simulate the Boolean-based blind condition:
        # If the input contains a classic "OR always true" pattern, we treat it as TRUE.
        is_true_payload = (
            "' or '1'='1" in normalized
            or "' or 1=1" in normalized
            or "' or 'a'='a" in normalized
            or "or 1=1--" in normalized
        )

        if is_true_payload:
            print("\n[Server Response] 👉 Welcome back, admin!\n")

            explanation = """
            Explanation (what happened behind the scenes):

            Original query:

                SELECT * FROM users
                WHERE username = 'admin'
                  AND password = '<USER_INPUT>';

            Your injected password (for example):

                ' OR '1'='1

            The WHERE condition becomes something like:

                WHERE username = 'admin'
                  AND (password = '' OR '1'='1')

            Because '1'='1' is always TRUE, the overall condition becomes TRUE
            for the 'admin' row, so the application logs you in.

            This is called BLIND SQL injection because:
              - You only saw "Welcome back, admin!" vs "Invalid login."
              - You didn't see any SQL error or actual data from the DB,
                but you could still manipulate the logic.

            In real attacks, blind SQLi can be combined with clever payloads
            (AND substrings, comparisons, timing functions) to extract data
            one bit/character at a time.

            Defense:
              - Use parameterized queries (prepared statements).
              - Never concatenate user input into SQL.
              - Implement strong authentication & rate limiting.
            """
            print_wrapped(explanation)
            return True
        else:
            print("\n[Server Response] 👉 Invalid login.\n")
            if attempts < max_attempts:
                print(f"Try again... (attempt {attempts}/{max_attempts})\n")

    print("\nYou reached the maximum attempts for this level.")
    print_wrapped("""
    Example of a working blind SQLi payload (for learning):

        ' OR '1'='1

    or:

        ' OR 1=1--
    """)
    return False


def main():
    print("=" * 70)
    print("   SQL Injection Adventure - Level 4: Blind SQL Injection")
    print("=" * 70)

    disclaimer = """
    DISCLAIMER:
    This game is for EDUCATIONAL PURPOSES ONLY.
    Do NOT use these techniques on systems you do not own
    or do not have explicit permission to test.
    """
    print_wrapped(disclaimer)

    completed = level_4()

    print("=" * 70)
    print("Game Over")
    print("=" * 70)
    if completed:
        print("You completed Level 4! 🎉")
    else:
        print("Level 4 not completed. You can re-run and try again.")
    print("Thanks for playing and learning responsibly.")


if __name__ == "__main__":
    main()
