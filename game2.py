#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 2 (UNION-based Data Extraction)

Educational project to understand a basic UNION SELECT SQL injection payload.
"""

import textwrap


def print_wrapped(text: str) -> None:
    """Print nicely wrapped paragraphs."""
    print(textwrap.dedent(text).strip())
    print()


def level_2():
    print("=" * 70)
    print("LEVEL 2: UNION-based Data Extraction")
    print("=" * 70)

    description = """
    Scenario:

    You are testing a vulnerable search feature on a website.

    The backend runs this SQL query when a user types something
    into the search box:

        SELECT id, username FROM users
        WHERE username LIKE '%<SEARCH_TERM>%';

    The result is displayed in a table with 2 columns: id and username.

    Goal:
      Use a UNION-based SQL injection payload as <SEARCH_TERM> to
      extract data from another table:

          secrets(username, password)

      You want to show all usernames and passwords from `secrets`
      by combining your injected SELECT with the original one.

    Important rules:
      - The number of columns must match on both sides of UNION.
      - The original query selects 2 columns: (id, username)
      - Your injected SELECT must also return 2 columns.
      - You should comment out the rest of the original query using --.

    Hint:
      Think of a payload like:

          ' UNION SELECT username, password FROM secrets--

      This closes the original string, injects your UNION SELECT,
      and then comments out the trailing part of the query.
    """

    print_wrapped(description)

    max_attempts = 6
    attempts = 0

    while attempts < max_attempts:
        payload = input("Enter your SQL payload (or type 'hint' / 'quit'): ").strip()

        if payload.lower() == "quit":
            print("\nExiting game. Goodbye!")
            exit(0)

        if payload.lower() == "hint":
            print_wrapped("""
            Hint:
              - You need: 2 columns in your UNION SELECT (username, password)
              - Use: UNION SELECT username, password FROM secrets
              - End with: --  to comment out the rest
              - Wrap the whole thing in a starting quote: '
            Example pattern:
              ' UNION SELECT username, password FROM secrets--
            """)
            continue

        attempts += 1

        normalized = payload.lower().replace('"', "'").strip()

        # Very simple simulation, we just check if payload contains the needed structure
        required_parts = [
            "union select",
            "username",
            "password",
            "from secrets",
            "--",
        ]

        if all(part in normalized for part in required_parts) and normalized.startswith("'"):
            print("\n✅ SUCCESS! You extracted data using UNION-based SQL injection.\n")

            explanation = """
            What happened?

            Original vulnerable query:

                SELECT id, username FROM users
                WHERE username LIKE '%<SEARCH_TERM>%';

            Your injected payload (as <SEARCH_TERM>):

                ' UNION SELECT username, password FROM secrets--

            The final SQL the database sees looks like:

                SELECT id, username FROM users
                WHERE username LIKE '%'
                UNION SELECT username, password FROM secrets-- %';

            Key points:
              - The first SELECT returns (id, username)
              - The second SELECT (your injected one) returns (username, password)
              - Both have 2 columns, so UNION works.
              - The -- sequence starts a comment, so the trailing %'; part is ignored.

            The result:
              - The application now shows not only normal users,
                but also all rows from the `secrets` table, including passwords.

            This demonstrates how UNION-based SQL injection can be used to
            exfiltrate sensitive data from other tables.

            Defenses:
              - Use parameterized queries (prepared statements).
              - Limit or disable the use of UNION in queries where user input is involved.
              - Implement least-privilege DB accounts (so app cannot read every table).
            """
            print_wrapped(explanation)
            return True
        else:
            print("\n❌ That payload didn't work in our simulation.")
            if attempts < max_attempts:
                print(f"Try again... (attempt {attempts}/{max_attempts})\n")

    print("\nYou reached the maximum attempts for this level.")
    print("Here is an example of a working payload for learning:\n")
    print_wrapped("' UNION SELECT username, password FROM secrets--")
    return False


def main():
    print("=" * 70)
    print("   SQL Injection Adventure - Level 2: UNION-based Extraction")
    print("=" * 70)

    disclaimer = """
    DISCLAIMER:
    This game is for EDUCATIONAL PURPOSES ONLY.
    Do NOT use these techniques on systems you do not own
    or do not have explicit permission to test.
    """
    print_wrapped(disclaimer)

    completed = level_2()

    print("=" * 70)
    print("Game Over")
    print("=" * 70)
    if completed:
        print("You completed Level 2! 🎉")
    else:
        print("Level 2 not completed. You can re-run and try again.")
    print("Thanks for playing and learning responsibly.")


if __name__ == "__main__":
    main()
