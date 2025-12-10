#!/usr/bin/env python3
"""
SQL Injection Adventure - Level 7 (WAF / Filter Bypass)

Final boss level:
Simulates bypassing a simplistic input filter that blocks obvious SQL injection
keywords. The challenge is to craft obfuscated payloads that still inject logic.
"""

import textwrap
import re


def print_wrapped(text: str):
    print(textwrap.dedent(text).strip())
    print()


def waf_blocks(payload):
    """
    Simple simulated filter/WAF that blocks obvious patterns.
    (Real WAFs are far more complex — this is for teaching.)
    """
    blocked_patterns = [
        r"union",
        r"sleep",
        r"or 1=1",
        r"' or '1'='1",
        r"select",
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, payload, flags=re.IGNORECASE):
            return True
    return False


def evaluate_obfuscated(payload):
    """
    If the payload contains obfuscated versions like:
    UNI/**/ON
    SL/**/EEP
    OR/**/1=1
    and begins with a quote, we count it as success for this simulation.
    """

    normalized = payload.lower().replace(" ", "")
    bypass_patterns = [
        "uni/**/on",     # Obfuscated UNION
        "sl/**/eep",     # Obfuscated SLEEP
        "or/**/1=1",     # OR 1=1 bypass
    ]

    return any(bp in normalized for bp in bypass_patterns)


def level_7():
    print("=" * 70)
    print("LEVEL 7: WAF / Filter Bypass")
    print("=" * 70)

    intro = """
    Scenario:

    The target system now uses a basic Web Application Firewall (WAF).

    It blocks SQL injection attempts containing:
        - UNION
        - SELECT
        - OR 1=1
        - ' OR '1'='1
        - SLEEP

    However...

    The filter is naive — it only blocks these exact patterns.

    Your mission:
      Craft an obfuscated payload that EXECUTES the same logic
      WITHOUT containing the banned words in plain form.

    Example ideas hackers use:
        UNI/**/ON
        SL/**/EEP
        OR/**/1=1

    Try entering payloads that bypass the naive filter.
    """

    print_wrapped(intro)

    while True:
        payload = input("\nEnter your payload (or 'hint' / 'quit'): ").strip()

        if payload.lower() == "quit":
            print("\nExiting final level.")
            return False

        if payload.lower() == "hint":
            print_wrapped("""
            Hint:
              - WAF blocks lowercase 'union', but you can break it:

                    UNI/**/ON

              - Blocks OR 1=1, try:

                    OR/**/1=1

              - Blocks SLEEP but not:

                    SL/**/EEP(5)
            """)
            continue

        if waf_blocks(payload):
            print("\n🚫 BLOCKED by WAF — Try a more clever payload.")
            continue

        if evaluate_obfuscated(payload):
            print("\n🔥 SUCCESS! You bypassed the naive WAF.")
            break
        else:
            print("\n❌ Not a recognized bypass type — try again.")

    print("\n" + "=" * 70)
    print("FINAL EXPLANATION")
    print("=" * 70)

    explanation = """
    What happened?

    Your payload bypassed the naive filter by splitting or encoding keywords.

    Real attacker techniques include:
      - Comment injection: UNI/**/ON
      - URL encoding: %75%6E%69%6F%6E
      - Case swapping: UnIoN SeLeCt
      - Whitespace tricks: UNION%0ASELECT
      - Function aliasing: sleep() → pg_sleep() → benchmark()

    Why this works:
      Naive filters only block exact words.
      Attackers mutate payloads without changing logic.

    Real defenses:
      - Parameterized queries
      - Server-side allowlists (not blocklists)
      - Normalizing input before inspecting
      - Real WAFs + anomaly detection
    """

    print_wrapped(explanation)
    return True


def main():
    print("=" * 70)
    print("   SQL Injection Adventure - Level 7: WAF Bypass")
    print("=" * 70)

    disclaimer = """
    FINAL DISCLAIMER:
    This project is for EDUCATIONAL PURPOSES ONLY.
    Do NOT test these techniques on real systems without explicit authorization.
    """
    print_wrapped(disclaimer)

    level_7()

    print("=" * 70)
    print("🎉 GAME OVER — YOU COMPLETED ALL LEVELS 🎉")
    print("=" * 70)


if __name__ == "__main__":
    main()
