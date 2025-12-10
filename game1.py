#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 1 (Login Bypass)

Educational project to understand a basic SQL injection payload.
"""

import textwrap


def print_wrapped(text: str) -> None:
    """Print nicely wrapped paragraphs."""
    print(textwrap.dedent(text).strip())
    print()


def level_1():
    print("=" * 60)
    print("LEVEL 1: Classic Login Bypass")
    print("=" * 60)

    description = """
    You are attacking a vulnerable login form.

    The backend builds this SQL query using your input:

        SELECT * FROM users
        WHERE username = '<USERNAME>'
          AND password = '<PASSWORD>';

    The developer has made a big mistake: they are directly
    concatenating your input into the query.

    Goal to:
      Log in without knowing any real username or password.

    Hint:
      Try to make the WHERE condition always TRUE by using a payload
      like: ' OR '1'='1
    """

    print_wrapped(description)

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        print("Enter the SAME payload for both username and password.")
        payload = input("Your SQL payload (or type 'hint' / 'quit'): ").strip()

        if payload.lower() == "quit":
            print("\nExiting game. Goodbye!")
            exit(0)
        if payload.lower() == "hint":
            print_wrapped("Hint: Try something like: ' OR '1'='1")
            continue

        attempts += 1

        # Check if the payload contains our classic login bypass pattern
        if "' or '1'='1" in payload.lower() or "' or 1=1" in payload.lower():
            print("\n✅ SUCCESS!")
            explanation = """
            What happened?

            The vulnerable query becomes something like:

                SELECT * FROM users
                WHERE username = '' OR '1'='1'
                  AND password = '' OR '1'='1';

            Because '1'='1' is always TRUE, the whole WHERE condition
            becomes TRUE, so the database returns at least one user row.

            The application thinks you are logged in.

            This is why directly concatenating user input into SQL queries
            is extremely dangerous. The fix is to use parameterized queries
            (prepared statements) so that input is always treated as data,
            not as code.
            """
            print_wrapped(explanation)
            return True
        else:
            print("\n❌ That payload didn't work in our simulation.")
            if attempts < max_attempts:
                print(f"Try again... (attempt {attempts}/{max_attempts})\n")

    print("\nYou reached the maximum attempts for this level.")
    print("Here is the classic solution for learning purposes:\n")
    print_wrapped("' OR '1'='1")
    return False


def main():
    print("=" * 60)
    print("   SQL Injection Adventure - Level 1: Login Bypass")
    print("=" * 60)

    disclaimer = """
    DISCLAIMER:
    This game is for EDUCATIONAL PURPOSES ONLY.
    Do NOT use these techniques on systems you do not own
    or do not have explicit permission to test.
    """
    print_wrapped(disclaimer)

    completed = level_1()

    print("=" * 60)
    print("Game Over")
    print("=" * 60)
    if completed:
        print("You completed Level 1! 🎉")
    else:
        print("Level 1 not completed. You can re-run and try again.")
    print("Thanks for playing and learning responsibly.")


if __name__ == "__main__":
    main()
