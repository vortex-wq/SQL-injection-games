#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 6 (Blind SQLi Manual Extraction)

Educational project to understand how attackers can extract a secret value
(e.g., admin password) one character at a time using ONLY TRUE/FALSE style
responses (no direct SQL errors or data output).
"""

import textwrap


def print_wrapped(text: str) -> None:
    print(textwrap.dedent(text).strip())
    print()


def level_6():
    print("=" * 70)
    print("LEVEL 6: Blind SQL Injection - Manual Data Extraction")
    print("=" * 70)

    # In a real attack, the attacker does NOT know this.
    secret_password = "S3cr3t!"
    password_length = len(secret_password)

    description = f"""
    Scenario:

    There is an 'admin' account with a secret password stored in the database.
    The application runs a query like:

        SELECT * FROM users
        WHERE username = 'admin'
          AND password = '<USER_INPUT>';

    You cannot see:
      - Any SQL errors
      - Any output or data from the database

    You only see a generic message like:
      - "Login success"  (TRUE)
      - "Login failed"   (FALSE)

    However, as an attacker, you can craft payloads that ask questions
    about the password one character at a time, for example:

        Does the 1st character of the password equal 'S' ?
        Does the 1st character equal 'A' ?
        Does the 2nd character equal '3' ?
        ...

    In SQL this might look like (MySQL-style):

        ' AND SUBSTR(password, 1, 1) = 'S'--
        ' AND SUBSTR(password, 2, 1) = '3'--
        ' AND SUBSTR(password, 3, 1) = 'c'--

    Or with time-based logic:

        ' AND IF(SUBSTR(password, 1, 1)='S', SLEEP(5), 0)--

    In this level, we will simulate this behaviour:

      - There is a SECRET PASSWORD of length {password_length}.
      - You will specify:
          1) A position index (1 to {password_length})
          2) A character guess for that position
      - The server will respond ONLY:
          - "Condition TRUE"  (if your guess matches that character)
          - "Condition FALSE" (if your guess is wrong)

    Your goal:
      Manually reconstruct the full password using as few guesses as you can.
    """

    print_wrapped(description)

    print_wrapped(f"Note: For this demo, the secret password length is {password_length} characters.\n")

    # We keep track of what the player has discovered so far.
    discovered = ["?"] * password_length
    max_rounds = 40
    rounds = 0

    while rounds < max_rounds:
        print("=" * 70)
        print("Current discovered password state:")
        print("  " + "".join(discovered))
        print(f"( '?' means unknown, length = {password_length} )")
        print("=" * 70)

        # Ask for position
        pos_input = input(f"Enter position to test (1-{password_length}), or 'done' / 'hint' / 'quit': ").strip()

        if pos_input.lower() == "quit":
            print("\nExiting level. Goodbye.")
            return False

        if pos_input.lower() == "hint":
            print_wrapped("""
            Hint:
              - Try different positions from 1 to password_length.
              - For each position, test different characters (a-z, A-Z, 0-9, symbols).
              - When the server says 'Condition TRUE', you found the correct character
                at that position.
            """)
            continue

        if pos_input.lower() == "done":
            guess = input("Enter your full guessed password: ").strip()
            if guess == secret_password:
                print("\n🎉 Correct! You successfully reconstructed the secret password.")
                break
            else:
                print("\n❌ That is not the correct password. Keep trying.")
                continue

        if not pos_input.isdigit():
            print("\nPlease enter a valid number for position.\n")
            continue

        pos = int(pos_input)
        if not (1 <= pos <= password_length):
            print(f"\nPosition must be between 1 and {password_length}.\n")
            continue

        char_guess = input(f"Enter your character guess for position {pos}: ").strip()
        if len(char_guess) != 1:
            print("\nPlease enter exactly ONE character as your guess.\n")
            continue

        rounds += 1
        actual_char = secret_password[pos - 1]

        # Simulated TRUE/FALSE result
        if char_guess == actual_char:
            print("\n[Server response] Condition TRUE (your comparison matched).")
            discovered[pos - 1] = char_guess
        else:
            print("\n[Server response] Condition FALSE (your comparison did not match).")

        # Check if the player has fully discovered the password
        if "".join(discovered) == secret_password:
            print("\n✅ You have discovered every character of the secret password!")
            break

        print(f"\nRounds used: {rounds}/{max_rounds}\n")

    print("\n" + "=" * 70)
    print("Level 6 Summary & Explanation")
    print("=" * 70)

    explanation = f"""
    The secret password was: {secret_password}

    In a real blind SQL injection attack, an attacker would NOT be told the
    password directly. Instead, they would:

      1) Pick a position index i (1, 2, 3, ...)
      2) For each possible character c in [a-zA-Z0-9...]:
            Ask the database:

                Does SUBSTR(password, i, 1) = 'c' ?

         Example (MySQL Boolean-based):

                ' AND SUBSTR(password, {1}, 1) = 'S'--

         or Time-based:

                ' AND IF(SUBSTR(password, {1}, 1)='S', SLEEP(5), 0)--

      3) Observe:
            - TRUE vs FALSE behaviour
            - Or SLOW vs FAST responses

      4) When a guess (i, c) makes the condition TRUE (or slow), they know:
            password[i] = c

      5) Repeat for each position until the entire secret is recovered.

    This level simulated exactly that:
      - You chose a position.
      - You guessed a character.
      - The server only told you TRUE/FALSE (no data, no errors, no prints).

    This is how powerful blind SQL injection can be:
      - Even when the application hides errors.
      - Even when it never prints database contents.
      - Data can still be exfiltrated bit-by-bit using logic and timing.

    Defenses:
      - Use parameterized queries everywhere.
      - Limit DB user privileges (so even if injected, damage is limited).
      - Apply rate limits and anomaly detection for suspicious repetitive patterns.
      - Avoid exposing even simple TRUE/FALSE differences when possible.
    """

    print_wrapped(explanation)
    return True


def main():
    print("=" * 70)
    print("   SQL Injection Adventure - Level 6: Blind Data Extraction")
    print("=" * 70)

    disclaimer = """
    DISCLAIMER:
    This game is for EDUCATIONAL PURPOSES ONLY.
    Do NOT use these techniques on systems you do not own
    or do not have explicit permission to test.
    """
    print_wrapped(disclaimer)

    level_6()

    print("=" * 70)
    print("Game Over - Level 6")
    print("=" * 70)
    print("Thanks for playing and learning responsibly.")


if __name__ == "__main__":
    main()
