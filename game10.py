#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 10 (Final Boss Exam)

You face three chained challenges:
  1) Classic login bypass
  2) UNION-based data extraction
  3) Time-based blind SQL injection

Beat all three to clear the final level.
"""

import textwrap
import time


def print_wrapped(text: str) -> None:
    print(textwrap.dedent(text).strip())
    print()


def stage_1_login_bypass():
    print("=" * 70)
    print("STAGE 1: Classic Login Bypass")
    print("=" * 70)

    desc = """
    Target:

      A vulnerable login form uses:

          SELECT * FROM users
          WHERE username = '<USER>'
            AND password = '<PASS>';

    You control BOTH username and password fields.

    Goal:
      Bypass login WITHOUT knowing any real credentials by making
      the WHERE condition always TRUE.

    Example idea:
      A payload like ' OR '1'='1
    """
    print_wrapped(desc)

    attempts = 5
    while attempts > 0:
        payload = input("Enter payload for BOTH username and password (or 'hint' / 'quit'): ").strip()
        if payload.lower() == "quit":
            print("\nYou gave up on Stage 1.")
            return False
        if payload.lower() == "hint":
            print_wrapped("""
            Hint:
              Try something like:

                  ' OR '1'='1
            """)
            continue

        norm = payload.lower().replace('"', "'")

        if "' or '1'='1" in norm or "' or 1=1" in norm:
            print_wrapped("""
            ✅ Stage 1 passed!

            Your payload turned the WHERE clause into something like:

                WHERE username = '' OR '1'='1'
                  AND password = '' OR '1'='1';

            Since '1'='1' is always TRUE, the query returns at least one row,
            and the app treats you as authenticated.

            On to Stage 2...
            """)
            return True

        attempts -= 1
        print(f"❌ Nope. Attempts left: {attempts}\n")

    print("\nYou failed Stage 1. Review earlier levels and try again.")
    return False


def stage_2_union_extraction():
    print("=" * 70)
    print("STAGE 2: UNION-based Data Extraction")
    print("=" * 70)

    desc = """
    Target:

      A search feature uses:

          SELECT id, username
          FROM users
          WHERE username LIKE '%<SEARCH>%';

      Results are shown in a table with 2 columns.

      You suspect another table 'secrets' exists:

          secrets(username, password)

    Goal:
      Inject a UNION-based payload into <SEARCH> that:

        - Keeps column count = 2
        - Extracts username + password from secrets
        - Comments out the rest of the query

    Example pattern:

        ' UNION SELECT username, password FROM secrets--
    """
    print_wrapped(desc)

    attempts = 6
    while attempts > 0:
        payload = input("Enter your search term payload (or 'hint' / 'quit'): ").strip()
        if payload.lower() == "quit":
            print("\nYou gave up on Stage 2.")
            return False
        if payload.lower() == "hint":
            print_wrapped("""
            Hint:
              - Use: UNION SELECT username, password FROM secrets
              - 2 columns only
              - End with: --
              - Start with a quote to break out of the string

              Example:
                ' UNION SELECT username, password FROM secrets--
            """)
            continue

        norm = payload.lower().replace('"', "'")

        needed = all(
            part in norm
            for part in [
                "'",            # starts with a quote somewhere
                "union select",
                "username",
                "password",
                "from secrets",
                "--",
            ]
        )

        if needed and norm.strip().startswith("'"):
            print_wrapped("""
            ✅ Stage 2 passed!

            Your payload produced a query like:

                SELECT id, username
                FROM users
                WHERE username LIKE '%'
                UNION SELECT username, password FROM secrets-- %';

            The UNION SELECT returns (username, password) from the secrets table,
            and because both queries have 2 columns, the DB accepts it.

            Now the app's result table can include sensitive data.

            On to Stage 3...
            """)
            return True

        attempts -= 1
        print(f"❌ That did not simulate a valid UNION-based exfiltration. Attempts left: {attempts}\n")

    print("\nYou failed Stage 2. Review UNION-based SQLi and try again.")
    return False


def stage_3_time_based():
    print("=" * 70)
    print("STAGE 3: Time-based Blind SQL Injection")
    print("=" * 70)

    desc = """
    Target:

      A login endpoint runs:

          SELECT * FROM users
          WHERE username = 'admin'
            AND password = '<PASS>';

      The response body is always the same "OK", but:

        - If the condition is TRUE, DB returns quickly.
        - If you inject SLEEP() into a TRUE condition,
          the response is noticeably slower.

    Goal:
      Craft a password payload that contains a time-delay function
      (like SLEEP or pg_sleep), combined with OR logic, to simulate a
      time-based blind SQL injection.

    Example idea (MySQL-style):

        ' OR IF(1=1, SLEEP(5), 0)--

    or a simpler one like:

        ' OR SLEEP(5)--
    """
    print_wrapped(desc)

    attempts = 6
    while attempts > 0:
        pwd = input("Enter password payload for admin (or 'hint' / 'quit'): ").strip()
        if pwd.lower() == "quit":
            print("\nYou gave up on Stage 3.")
            return False
        if pwd.lower() == "hint":
            print_wrapped("""
            Hint:
              Look for:
                - OR 1=1 or another always-true condition
                - A time function like SLEEP(5) or pg_sleep(5)
                - Comment at the end: --

              Example:
                ' OR IF(1=1, SLEEP(5), 0)--
                ' OR SLEEP(5)--
            """)
            continue

        norm = pwd.lower().replace('"', "'")

        is_time_payload = ("sleep(" in norm or "pg_sleep(" in norm) and "or" in norm

        print("\n[Server] Processing request...")
        start = time.time()

        if is_time_payload:
            time.sleep(2)  # simulate SLEEP(5) with shorter delay
            end = time.time()
            elapsed = end - start
            print(f"[Server] Response delayed... (simulated {elapsed:.2f} seconds)")
            print_wrapped("""
            ✅ Stage 3 passed!

            Your payload included a time-delay function combined with OR logic.
            In a real DB, something like:

                ' OR IF(1=1, SLEEP(5), 0)--

            would cause the WHERE condition to evaluate TRUE and execute SLEEP(5),
            making the response much slower.

            By measuring response times, attackers can infer TRUE/FALSE conditions
            and slowly extract data in a blind scenario.

            You've completed the Final Boss Exam. 🎉
            """)
            return True

        else:
            end = time.time()
            elapsed = end - start
            print(f"[Server] Quick response (elapsed {elapsed:.2f} seconds)")
            attempts -= 1
            print(f"❌ That didn't trigger a simulated time-based condition. Attempts left: {attempts}\n")

    print("\nYou failed Stage 3. Review time-based blind SQLi and try again.")
    return False


def final_boss():
    print("=" * 70)
    print("SQL Injection Adventure - Level 10: Final Boss Exam")
    print("=" * 70)

    intro = """
    Welcome to the Final Boss.

    You will face THREE stages:

      1) Classic login bypass
      2) UNION-based data extraction
      3) Time-based blind SQL injection

    Pass all three to clear the SQL Injection Adventure.
    """
    print_wrapped(intro)

    score = 0
    total = 3

    if stage_1_login_bypass():
        score += 1
    else:
        print_wrapped("\nYou can still continue to try the next stages for practice.\n")

    if stage_2_union_extraction():
        score += 1
    else:
        print_wrapped("\nStage 2 not cleared, but you can still attempt Stage 3.\n")

    if stage_3_time_based():
        score += 1

    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Stages cleared: {score}/{total}")

    if score == total:
        print_wrapped("""
        🎉 PERFECT CLEAR!

        You demonstrated understanding of:
          - Boolean-based login bypass
          - UNION-based exfiltration
          - Time-based blind SQLi

        Combined with earlier levels (enumeration, second-order, WAF bypass,
        and defender mode), you now have a solid foundation in SQL injection
        from both offensive and defensive perspectives.
        """)
    else:
        print_wrapped("""
        Not a perfect run, but that's fine — this is how you learn.

        Revisit the earlier levels (especially 1, 2, 5) and then come back
        to beat the Final Boss again. Real hackers and defenders iterate.
        """)


def main():
    disclaimer = """
    DISCLAIMER:
      This project is for EDUCATIONAL PURPOSES ONLY.
      Do NOT use these techniques on systems you do not own
      or do not have explicit permission to test.
    """
    print_wrapped(disclaimer)
    final_boss()


if __name__ == "__main__":
    main()
