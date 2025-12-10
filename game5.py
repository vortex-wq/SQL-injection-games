#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 5 (Time-based Blind SQL Injection)

Educational project to understand how attackers use time delays (SLEEP)
to infer TRUE/FALSE conditions when there is no visible error or data output.
"""

import textwrap
import time


def print_wrapped(text: str) -> None:
    print(textwrap.dedent(text).strip())
    print()


def level_5():
    print("=" * 70)
    print("LEVEL 5: Time-based Blind SQL Injection")
    print("=" * 70)

    description = """
    Scenario:

    You are testing an API endpoint that behaves like this:

        SELECT * FROM users
        WHERE username = 'admin'
          AND password = '<USER_INPUT>';

    BUT:
      - You do NOT see error messages.
      - You do NOT see query results.
      - The HTTP response body is always just: "OK".

    The ONLY thing you can observe:
      - How long the server takes to respond.

    Idea (time-based blind SQLi):

      If a condition is TRUE, force the database to SLEEP for a few seconds.
      If it's FALSE, return immediately.

      Examples (MySQL style):

        ' OR IF(1=1, SLEEP(5), 0)--    -- slow response (TRUE)
        ' OR IF(1=2, SLEEP(5), 0)--    -- fast response (FALSE)

    In a real attack, you might ask:
      - Is the first letter of the admin password 'a'?
      - If TRUE: SLEEP(5), else return quickly.
      - Measure response time to learn each character.

    Goal for this level:
      Enter a password payload that would cause a time delay when the condition
      evaluates to TRUE. We will simulate the delay when we detect a SLEEP-style
      payload in your input.
    """

    print_wrapped(description)

    max_attempts = 6
    attempts = 0

    while attempts < max_attempts:
        pwd = input("Enter password for admin (or 'hint' / 'quit'): ").strip()

        if pwd.lower() == "quit":
            print("\nExiting game. Goodbye!")
            exit(0)

        if pwd.lower() == "hint":
            print_wrapped("""
            Hint:
              - Use a payload that calls a time delay function such as SLEEP().
              - Common patterns:

                    ' OR IF(1=1, SLEEP(5), 0)--
                    ' OR SLEEP(5)--

              - Some databases use different names, e.g. pg_sleep() in PostgreSQL.
            """)
            continue

        attempts += 1

        normalized = pwd.lower().replace('"', "'").strip()

        # We simulate detection of a time-based payload.
        # If the payload contains "sleep(" or "pg_sleep(" and an "or" condition,
        # we treat it as a time-based blind SQLi.
        is_time_based = (
            "sleep(" in normalized or "pg_sleep(" in normalized
        ) and "or" in normalized

        print("\n[Server] Received request. Processing...")

        start = time.time()

        if is_time_based:
            # Simulate a noticeable delay to mimic SLEEP()
            time.sleep(2)  # shorter than real SLEEP(5), just for demo
            end = time.time()
            elapsed = end - start

            print(f"[Server] Response delayed... (simulated {elapsed:.2f} seconds)")
            print("\n[Client perspective] 🤔 The server responded much slower than usual.")
            explanation = """
            Explanation:

            Your payload contained a time-delay function (like SLEEP or pg_sleep)
            combined with an OR condition. In a real database, something like:

                ' OR IF(1=1, SLEEP(5), 0)--    -- MySQL

            would turn the WHERE clause into:

                WHERE username = 'admin'
                  AND (password = '' OR IF(1=1, SLEEP(5), 0))

            Because 1=1 is TRUE, the IF condition triggers SLEEP(5), delaying
            the response. You, as the attacker, see that the page took much
            longer to load, which tells you the condition evaluated to TRUE.

            By changing the condition (e.g., checking each character of a password),
            attackers can slowly extract data from the database without ever
            seeing errors or direct query results. They only need timing.

            This is time-based blind SQL injection.

            Defense:
              - Use parameterized queries (prepared statements).
              - Avoid allowing user input to influence control functions
                like SLEEP(), BENCHMARK(), pg_sleep(), etc.
              - Use rate limiting and anomaly detection for suspicious delays.
            """
            print_wrapped(explanation)
            return True
        else:
            end = time.time()
            elapsed = end - start
            print(f"[Server] Quick response. (elapsed {elapsed:.2f} seconds)")
            print("[Client perspective] ✅ Looks like a normal fast response.\n")
            if attempts < max_attempts:
                print(f"That did NOT trigger a time-based condition. Attempts left: {attempts}/{max_attempts}\n")

    print("\nYou reached the maximum attempts for this level.")
    print_wrapped("""
    Example of a working time-based blind SQLi payload (for learning):

        ' OR IF(1=1, SLEEP(5), 0)--

    or (PostgreSQL-style):

        ' OR CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END--
    """)

    return False


def main():
    print("=" * 70)
    print("   SQL Injection Adventure - Level 5: Time-based Blind SQLi")
    print("=" * 70)

    disclaimer = """
    DISCLAIMER:
    This game is for EDUCATIONAL PURPOSES ONLY.
    Do NOT use these techniques on systems you do not own
    or do not have explicit permission to test.
    """
    print_wrapped(disclaimer)

    completed = level_5()

    print("=" * 70)
    print("Game Over")
    print("=" * 70)
    if completed:
        print("You completed Level 5! 🎉")
    else:
        print("Level 5 not completed. You can re-run and try again.")
    print("Thanks for playing and learning responsibly.")


if __name__ == "__main__":
    main()
