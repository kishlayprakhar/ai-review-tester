from groq import Groq
import os
import json
from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print(GROQ_API_KEY)
SYSTEM_PROMPT = """
You are a senior software engineer with 10+ years of experience doing
thorough code reviews. You will be given a GitHub Pull Request diff.

Analyze it carefully and return ONLY a JSON object — no explanation,
no markdown, no backticks. Just raw JSON in this exact format:

{
  "bugs": [
    {
      "line": "approximate line or function name",
      "description": "what the bug is and why it matters",
      "severity": "critical / high / medium / low"
    }
  ],
  "improvements": [
    {
      "description": "what can be improved and exactly how to fix it"
    }
  ],
  "security_issues": [
    {
      "description": "the security risk and how to fix it"
    }
  ],
  "quality_score": 7,
  "summary": "A 2-3 sentence overall review of the code changes."
}

Rules you must follow:
- Return ONLY the JSON object. No text before or after it.
- Do NOT wrap the JSON in markdown code blocks or backticks.
- If there are no bugs, return an empty array: "bugs": []
- If there are no security issues, return: "security_issues": []
- quality_score must be a number from 1 to 10.
- Be specific: mention exact variable names and function names.

Severity definitions:
- critical : causes crash, data loss, or security breach
- high     : likely to cause bugs in production
- medium   : bad practice or code smell
- low      : minor style or readability issue
"""

# ── Validate Key ──────────────────────────────────────────────────────────────

def validate_groq_key():
    """
    Check that GROQ_API_KEY is set and not a placeholder.
    Exits with a helpful message if something is wrong.
    """
    if not GROQ_API_KEY:
        print("❌ ERROR: GROQ_API_KEY not found in .env file.")
        print("   Add this line to your .env file:")
        print("   GROQ_API_KEY=your_actual_key_here")
        print()
        print("   Get a free key at: console.groq.com")
        exit(1)

    if GROQ_API_KEY == "your_groq_key_here":
        print("❌ ERROR: You haven't replaced the placeholder key.")
        print("   Go to console.groq.com → API Keys → Create → paste in .env")
        exit(1)

    print("✅ Groq API key loaded from .env\n")

# ── Groq Client ───────────────────────────────────────────────────────────────

def get_groq_client():
    """
    Create and return an authenticated Groq client.
    """
    client = Groq(api_key=GROQ_API_KEY)
    return client

# ── Build the Prompt ──────────────────────────────────────────────────────────

def build_prompt(diff_data):
    """
    Convert the diff data from Week 1 into a readable text prompt.

    Parameters:
        diff_data (list): List of file diffs from get_pr_diff()

    Returns:
        str: Formatted prompt string ready to send to Groq
    """
    prompt = "Please review the following Pull Request diff:\n\n"

    for file in diff_data:
        prompt += f"### File: {file['filename']}\n"
        prompt += f"Status : {file['status']}\n"
        prompt += f"Changes: +{file['additions']} additions, -{file['deletions']} deletions\n\n"

        if file.get('patch'):
            prompt += "```diff\n"
            prompt += file['patch']
            prompt += "\n```\n\n"
        else:
            prompt += "(No diff available for this file)\n\n"

    return prompt

# ── Clean the Response ────────────────────────────────────────────────────────

def clean_response(raw_text):
    """
    Strip markdown code fences from the response if present.
    Sometimes the model wraps JSON in ```json ... ``` even when told not to.

    Parameters:
        raw_text (str): The raw string returned by the model

    Returns:
        str: Clean JSON string ready for json.loads()
    """
    text = raw_text.strip()

    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:-1]
        text  = "\n".join(lines)

    return text.strip()

# ── Send to Groq ──────────────────────────────────────────────────────────────

def get_code_review(diff_data):
    """
    Main function — sends the PR diff to Groq and returns a structured review.

    Parameters:
        diff_data (list): List of file diffs from get_pr_diff()

    Returns:
        dict: Review with keys: bugs, improvements, security_issues,
              quality_score, summary
        None: If something goes wrong
    """
    validate_groq_key()

    client = get_groq_client()
    prompt = build_prompt(diff_data)

    print("🤖 Sending diff to Groq (LLaMA 3 70B) for review...")
    print(f"   Files being reviewed: {len(diff_data)}")

    try:
        # Send to Groq using LLaMA 3 70B model
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",     # Free, powerful, great at code
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.3,             # Lower = more consistent JSON output
            max_tokens=2000
        )

        raw_text = response.choices[0].message.content
        print("✅ Groq responded!\n")

        # Clean and parse the response
        cleaned = clean_response(raw_text)
        review  = json.loads(cleaned)

        return review

    except json.JSONDecodeError:
        print("⚠️  Groq didn't return valid JSON.")
        print("   Raw response was:")
        print("-" * 40)
        print(raw_text)
        print("-" * 40)
        print("   Try running again — this usually fixes itself.")
        return None

    except Exception as e:
        print(f"❌ Groq API error: {e}")
        print("   Possible reasons:")
        print("   - API key is incorrect or expired")
        print("   - Rate limit hit (wait 1 minute and retry)")
        print("   - No internet connection")
        return None

# ── Test Block ────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print()
    print("=" * 52)
    print("  🤖 Testing Groq API — claude_utils.py")
    print("=" * 52)
    print()

    # Fake diff data — no GitHub needed to test this
    sample_diff = [
        {
            "filename"  : "app.py",
            "status"    : "modified",
            "additions" : 5,
            "deletions" : 2,
            "patch"     : (
                "@@ -10,7 +10,10 @@\n"
                " def divide(a, b):\n"
                "-    return a / b\n"
                "+    if b == 0:\n"
                "+        return None\n"
                "+    result = a / b\n"
                "+    return result\n"
            )
        },
        {
            "filename"  : "utils.py",
            "status"    : "modified",
            "additions" : 3,
            "deletions" : 1,
            "patch"     : (
                "@@ -5,5 +5,7 @@\n"
                " def get_user(id):\n"
                "-    return db.query(f'SELECT * FROM users WHERE id={id}')\n"
                "+    query = 'SELECT * FROM users WHERE id = ?'\n"
                "+    return db.execute(query, (id,))\n"
            )
        }
    ]

    print("📋 Using 2 sample files for testing:")
    print("   1. app.py   — divide by zero fix")
    print("   2. utils.py — SQL injection fix")
    print()

    review = get_code_review(sample_diff)

    if review:
        print("🎉 Review received successfully!")
        print()
        print(json.dumps(review, indent=2))
        print()
        print(f"  ⭐ Quality Score   : {review.get('quality_score')}/10")
        print(f"  🐛 Bugs Found     : {len(review.get('bugs', []))}")
        print(f"  ⚡ Improvements   : {len(review.get('improvements', []))}")
        print(f"  🔒 Security Issues: {len(review.get('security_issues', []))}")
        print()
        print("✅ claude_utils.py is working correctly!")
        print("   Ready to connect to main.py in Day 5")
    else:
        print("❌ No review returned. Read the error messages above.")
