#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 3 (ORDER BY Column Discovery)

Educational project to understand how attackers discover the number
of columns in a vulnerable SQL query using ORDER BY.
"""

import textwrap


def print_wrapped(text: str) -> None:
    print(textwrap.dedent(text).strip())
    print()


def level_3():
    print("=" * 70)
    print("LEVEL 3: Discovering Number of Columns with ORDER BY")
    print("=" * 70)

    description = """
    Scenario:

    The website uses a query like:

        SELECT id, username, email
        FROM users
        WHERE username = '<USER_INPUT>';

    You suspect the SELECT returns **3 columns** (id, username, email).

    Attack Strategy:
      Inject ORDER BY <number> to test how many columns exist.

    Try:
      ' ORDER BY 1--
      ' ORDER BY 2--
      ' ORDER BY 3--
      ' ORDER BY 4--  <-- should cause an error

    Goal:
      Use a payload that would cause an error because it requests a column index
      that doesn't exist.
    """

    print_wrapped(description)

    max_attempts = 5

    while max_attempts > 0:
        payload = input("Enter SQL payload (or 'hint' / 'quit'): ").strip()

        if payload.lower() == "quit":
            print("\nGoodbye.")
            exit()

        if payload.lower() == "hint":
            print_wrapped("Hint: A classic solution is: ' ORDER BY 4--")
            continue

        normalized = payload.lower().replace('"', "'").strip()

        if normalized.startswith("'") and "order by 4" in normalized and "--" in normalized:
            print("\n🔥 SUCCESS — You forced an error using ORDER BY 4\n")
            explanation = """
            Explanation:

            Your payload injected:

                ' ORDER BY 4--

            The final query becomes:

                SELECT id, username, email
                FROM users
                WHERE username = '' ORDER BY 4--';

            Because the SELECT has **only 3 columns**, ORDER BY 4 causes an error.

            This is how attackers discover the number of columns before performing
            UNION based extraction.

            Defense:
              - Parameterized queries
              - Do NOT concatenate input directly
              - Do NOT show raw error messages to users (they reveal structure)
            """
            print_wrapped(explanation)
            return True

        else:
            max_attempts -= 1
            print(f"❌ Not correct. Attempts left: {max_attempts}\n")

    print_wrapped("\nCorrect payload example (for learning): ' ORDER BY 4--")


def main():
    print("=" * 70)
    print("   SQL Injection Adventure - Level 3: ORDER BY Enumeration")
    print("=" * 70)
    level_3()
    print("\nThanks for playing!")
    print("=" * 70)


if __name__ == "__main__":
    main()
