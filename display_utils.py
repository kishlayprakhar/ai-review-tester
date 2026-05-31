

def display_review(review, pr_title=""):
    """
    Print the AI review in a clean, formatted way.

    Parameters:
        review   (dict): Parsed review from get_code_review()
        pr_title (str) : Title of the PR being reviewed
    """

    # Safety check — if no review came back, exit early
    if not review:
        print("⚠️  No review to display.")
        return

    # ── Header ─────────────────────────────────────────
    print()
    print("=" * 55)
    print("  🤖 AI Code Review")
    if pr_title:
        print(f"  📌 PR: {pr_title}")
    print("=" * 55)

    # ── Quality Score ───────────────────────────────────
    # Get score, default to 0 if missing
    score  = review.get("quality_score", 0)

    # Build a visual bar: ███████░░░
    filled = "█" * score
    empty  = "░" * (10 - score)

    # Pick a rating label based on the score
    if score >= 8:
        rating = "Excellent 🌟"
    elif score >= 6:
        rating = "Good 👍"
    elif score >= 4:
        rating = "Needs Work ⚠️"
    else:
        rating = "Poor ❌"

    print(f"\n  ⭐ Quality Score : {score}/10  [{filled}{empty}]  {rating}")

    # ── Summary ─────────────────────────────────────────
    print(f"\n  📝 Summary:")
    summary = review.get("summary", "No summary provided.")

    # Word wrap the summary neatly at 50 characters
    words = summary.split()
    line  = "  "
    for word in words:
        if len(line) + len(word) > 53:
            print(line)
            line = "  " + word + " "
        else:
            line += word + " "
    print(line)

    # ── Bugs ────────────────────────────────────────────
    bugs = review.get("bugs", [])
    print(f"\n  🐛 Bugs Found: {len(bugs)}")
    print("  " + "-" * 50)

    if bugs:
        # Map severity to an emoji for quick visual scanning
        severity_emoji = {
            "critical" : "🔴",
            "high"     : "🟠",
            "medium"   : "🟡",
            "low"      : "🟢"
        }
        for i, bug in enumerate(bugs, 1):
            severity = bug.get("severity", "medium").lower()
            emoji    = severity_emoji.get(severity, "⚪")

            print(f"  {i}. {emoji} [{severity.upper()}]")
            print(f"     {bug.get('description', 'No description')}")
            print(f"     📍 Location: {bug.get('line', 'Unknown')}")

            # Add spacing between bugs (but not after the last one)
            if i < len(bugs):
                print()
    else:
        print("  ✅ No bugs found!")

    # ── Improvements ────────────────────────────────────
    improvements = review.get("improvements", [])
    print(f"\n  ⚡ Improvements: {len(improvements)}")
    print("  " + "-" * 50)

    if improvements:
        for i, imp in enumerate(improvements, 1):
            print(f"  {i}. {imp.get('description', 'No description')}")
    else:
        print("  ✅ No improvements suggested!")

    # ── Security Issues ─────────────────────────────────
    security = review.get("security_issues", [])
    print(f"\n  🔒 Security Issues: {len(security)}")
    print("  " + "-" * 50)

    if security:
        for i, sec in enumerate(security, 1):
            print(f"  {i}. ⚠️  {sec.get('description', 'No description')}")
    else:
        print("  ✅ No security issues found!")

    # ── Footer ──────────────────────────────────────────
    print()
    print("=" * 55)
    print()


# ══════════════════════════════════════════════════════
# SECTION 2 — TEST BLOCK
# ══════════════════════════════════════════════════════
# Only runs when you execute THIS file directly:
#     python backend/display_utils.py
#
# Uses fake review data so you can test the display
# without needing Gemini or GitHub at all.

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("  🧪 Testing display_utils.py")
    print("=" * 55)
    print()

    # Fake review — same structure Gemini returns
    sample_review = {
        "bugs": [
            {
                "line"        : "divide(), app.py line 10",
                "description" : "Returning None on zero division may cause silent failures in calling code. Raise ValueError instead.",
                "severity"    : "medium"
            },
            {
                "line"        : "get_user(), utils.py line 5",
                "description" : "Variable 'id' is not validated before use — could cause unexpected behavior with negative values.",
                "severity"    : "low"
            }
        ],
        "improvements": [
            {
                "description" : "Add type hints to divide(a, b) — e.g. def divide(a: float, b: float) -> float"
            },
            {
                "description" : "Add docstrings to all functions explaining parameters and return values."
            },
            {
                "description" : "Consider using logging instead of returning None for error cases."
            }
        ],
        "security_issues": [
            {
                "description" : "utils.py previously used f-string in SQL query which is vulnerable to SQL injection. The parameterized fix is correct — ensure all other queries follow the same pattern."
            }
        ],
        "quality_score" : 7,
        "summary"       : "The PR addresses two important issues — a divide by zero case and a SQL injection vulnerability. The fixes are on the right track but could be more robust with proper error raising and type hints throughout."
    }

    # Call the display function with fake data
    display_review(sample_review, pr_title="Fix divide by zero and SQL injection")

    print("✅ display_utils.py is working correctly!")
    print("   Ready to be used in main.py")
    print()
