#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 9 (Second-Order SQL Injection)

This level demonstrates second-order SQL injection:
  - Malicious input is stored safely at first.
  - Later, another part of the app uses the stored value unsafely in a query.
"""

import textwrap


def print_wrapped(text: str) -> None:
    print(textwrap.dedent(text).strip())
    print()


def level_9():
    print("=" * 70)
    print("LEVEL 9: Second-Order SQL Injection (Stored Payload)")
    print("=" * 70)

    intro = """
    Scenario:

    Step 1: User Registration (seems safe)

      A web app lets you sign up and choose a display name:

          INSERT INTO profiles (user_id, display_name)
          VALUES (?, ?);

      Here, the developer correctly uses parameterized queries
      when inserting your display_name into the database.

      So even if you put something like:

          '; DROP TABLE users;--

      it is stored as DATA, not executed. So far: SAFE.

    Step 2: Admin Reporting (not so safe)

      Later, an admin uses a "User Report" feature with this code:

          # pseudo-code:

          stored_display_name = row.display_name  # read from DB

          sql = "SELECT * FROM profiles " \\
                "WHERE display_name = '" + stored_display_name + "';"

          db.query(sql)

      Here, stored_display_name is read from the database and concatenated
      directly into a new query.

      Now, if a malicious display_name (that you chose earlier) contains SQL,
      it gets concatenated into this new query and EXECUTES there.

      This is SECOND-ORDER SQL INJECTION:
        - Input seems harmless when stored.
        - It becomes dangerous only when reused elsewhere.

    Your goal in this level:

      1) Choose a "display name" that looks like a SQL injection payload.
      2) We'll simulate it being stored safely in the database.
      3) Then we simulate an admin report using that stored value in an
         unsafe concatenated query, causing an injection effect.

    Think of something like:

        '; DROP TABLE users;--
        ' OR '1'='1
    """

    print_wrapped(intro)

    display_name = input("Step 1 - Choose your display_name to register: ").strip()

    print_wrapped(f"""
    [Registration Phase]

    The app runs (parameterized):

        INSERT INTO profiles (user_id, display_name)
        VALUES (?, ?);

    with display_name = {repr(display_name)}

    Because it's parameterized, your input is stored as plain text, SAFE.
    No injection occurs at this stage.

    Your payload is now stored in the database, waiting...
    """)

    input("Press Enter to simulate the later admin action...")

    print_wrapped("""
    [Later... Admin Report Phase]

    Months later, a developer writes a quick-and-dirty admin tool:

        # WRONG way:
        sql = "SELECT * FROM profiles " \\
              "WHERE display_name = '" + stored_display_name + "';"

        db.query(sql)

    Here, stored_display_name is read from the database and concatenated
    directly into the new query.

    If your stored display_name contained SQL control characters, it will now
    be interpreted as PART OF THE QUERY.
    """)

    # Very simple check: if the stored display name contains typical SQLi chars,
    # we treat it as "successful second-order injection" for this simulation.
    lowered = display_name.lower()
    looks_malicious = any(
        token in lowered
        for token in ["' or ", "\" or ", " drop ", " union ", "--", ";"]
    )

    if looks_malicious:
        print_wrapped(f"""
        [Simulation Result]

        stored_display_name from DB = {repr(display_name)}

        Admin query becomes something like:

            SELECT * FROM profiles
            WHERE display_name = '{display_name}';

        Because your stored value includes SQL control sequences, this query
        is now BROKEN and potentially dangerous.

        In a real database, this could:

          - Bypass conditions (e.g., OR '1'='1')
          - Terminate the query and inject a second one (e.g., ; DROP TABLE users;--)
          - Leak or modify sensitive data

        ✅ This demonstrates a SECOND-ORDER SQL INJECTION:
           your payload was harmless when stored,
           but harmful when the app reused it unsafely later.
        """)
    else:
        print_wrapped(f"""
        [Simulation Result]

        stored_display_name from DB = {repr(display_name)}

        Admin query becomes something like:

            SELECT * FROM profiles
            WHERE display_name = '{display_name}';

        Your chosen display_name does NOT look like a typical SQL injection
        payload, so in this simulation it doesn't exploit the second-order flaw.

        However, the CODE is still vulnerable:
          - If any attacker had chosen a more malicious display_name earlier,
            the admin tool could be exploited later.

        ⚠ Even if YOUR input was safe, the pattern is dangerous.
        """)

    explanation = """
    Key Takeaways:

      • First-order SQL injection:
          The dangerous input is executed immediately in the same request.

      • Second-order SQL injection:
          - User input is stored (seemingly harmless).
          - Later, a different feature reuses that stored data unsafely in SQL.
          - Injection happens THEN, often in a different context (admin panel,
            cron job, reporting script, export, etc.).

    Why it's scary:
      - Security testing often focuses on the immediate effect of input.
      - Second-order bugs can hide until some rare code path uses stored data.
      - The attacker might not even be present when the exploit triggers.

    Defenses:
      - STILL use parameterized queries EVERYWHERE — not just on input insert,
        but also when building queries from stored data.
      - Treat DB-stored strings as untrusted if they originally came
        from user input.
      - Avoid adhoc string concatenation for admin/reporting tools.
      - Code review & security review for background jobs, admin panels,
        export scripts, and “quick internal tools”.

    Once bad data is inside your system, it can become a future weapon if
    you later assume it is safe and reuse it incorrectly.
    """
    print_wrapped(explanation)

    return True


def main():
    print("=" * 70)
    print("   SQL Injection Adventure - Level 9: Second-Order SQLi")
    print("=" * 70)

    disclaimer = """
    DISCLAIMER:
      This level demonstrates a more advanced and subtle form of SQL injection.
      As always, do NOT try these techniques on systems without explicit,
      written permission.
    """
    print_wrapped(disclaimer)

    level_9()

    print("=" * 70)
    print("Game Over - Level 9")
    print("=" * 70)
    print("You just learned about SECOND-ORDER SQL INJECTION. 🎯")


if __name__ == "__main__":
    main()
