

import sqlite3
import json
import os
from datetime import datetime


DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "reviews.db"
)


# ── Create Table ──────────────────────────────────────────────────────────────

def create_table():
    """
    Creates the reviews table if it doesn't already exist.
    Safe to call multiple times — won't duplicate the table.

    Table structure:
        id          → auto-increment primary key
        repo        → e.g. "psf/requests"
        pr_number   → e.g. 1234
        pr_title    → e.g. "Fix timeout handling"
        pr_author   → e.g. "somedev"
        pr_url      → GitHub URL of the PR
        review_json → full review stored as JSON string
        created_at  → timestamp when review was saved
    """
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            repo        TEXT    NOT NULL,
            pr_number   INTEGER NOT NULL,
            pr_title    TEXT,
            pr_author   TEXT,
            pr_url      TEXT,
            review_json TEXT    NOT NULL,
            created_at  TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ── Save Review ───────────────────────────────────────────────────────────────

def save_review(repo, pr_number, pr_title, pr_author, pr_url, review):
    """
    Save a new review to the database.

    Parameters:
        repo      (str) : GitHub repo e.g. "psf/requests"
        pr_number (int) : PR number e.g. 1234
        pr_title  (str) : Title of the PR
        pr_author (str) : GitHub username of PR author
        pr_url    (str) : URL of the PR
        review    (dict): Review dict from get_code_review()

    Returns:
        int: ID of the saved record
    """
    create_table()

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reviews
            (repo, pr_number, pr_title, pr_author, pr_url, review_json, created_at)
        VALUES
            (?, ?, ?, ?, ?, ?, ?)
    """, (
        repo,
        pr_number,
        pr_title,
        pr_author,
        pr_url,
        json.dumps(review),          # convert dict to JSON string
        datetime.now().isoformat()   # current timestamp
    ))

    record_id = cursor.lastrowid     # ID of the inserted row

    conn.commit()
    conn.close()

    return record_id


# ── Get Review by Repo + PR Number ───────────────────────────────────────────

def get_review(repo, pr_number):
    """
    Fetch the most recent review for a specific PR.
    Returns None if no review exists for this PR.

    Parameters:
        repo      (str): GitHub repo e.g. "psf/requests"
        pr_number (int): PR number e.g. 1234

    Returns:
        dict or None: Review data with all fields
    """
    create_table()

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, repo, pr_number, pr_title, pr_author,
               pr_url, review_json, created_at
        FROM reviews
        WHERE repo = ? AND pr_number = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (repo, pr_number))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id"         : row[0],
        "repo"       : row[1],
        "pr_number"  : row[2],
        "pr_title"   : row[3],
        "pr_author"  : row[4],
        "pr_url"     : row[5],
        "review"     : json.loads(row[6]),   # convert JSON string back to dict
        "created_at" : row[7]
    }


# ── Get All Reviews ───────────────────────────────────────────────────────────

def get_all_reviews():
    """
    Fetch all saved reviews ordered by most recent first.

    Returns:
        list: List of review dicts
    """
    create_table()

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, repo, pr_number, pr_title, pr_author,
               pr_url, review_json, created_at
        FROM reviews
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    reviews = []
    for row in rows:
        reviews.append({
            "id"         : row[0],
            "repo"       : row[1],
            "pr_number"  : row[2],
            "pr_title"   : row[3],
            "pr_author"  : row[4],
            "pr_url"     : row[5],
            "review"     : json.loads(row[6]),
            "created_at" : row[7]
        })

    return reviews


# ── Delete Review ─────────────────────────────────────────────────────────────

def delete_review(review_id):
    """
    Delete a review by its ID.

    Parameters:
        review_id (int): ID of the review to delete

    Returns:
        bool: True if deleted, False if not found
    """
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


# ── Test Block ────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print()
    print("=" * 52)
    print("  🗄️  Testing database.py — Week 3 Day 2")
    print("=" * 52)
    print()

    # Sample review data (same structure as Groq returns)
    sample_review = {
        "bugs": [
            {
                "line"        : "divide(), app.py",
                "description" : "Returns None on zero division",
                "severity"    : "medium"
            }
        ],
        "improvements": [
            {"description": "Add type hints to divide()"}
        ],
        "security_issues": [],
        "quality_score"  : 7,
        "summary"        : "Good fix but could raise exception instead of returning None."
    }

    # Test 1: Save a review
    print("🧪 Test 1: Saving a review...")
    record_id = save_review(
        repo      = "psf/requests",
        pr_number = 1234,
        pr_title  = "Fix timeout handling",
        pr_author = "somedev",
        pr_url    = "https://github.com/psf/requests/pull/1234",
        review    = sample_review
    )
    print(f"   ✅ Saved! Record ID: {record_id}\n")

    # Test 2: Fetch that review back
    print("🧪 Test 2: Fetching the review back...")
    fetched = get_review("psf/requests", 1234)
    if fetched:
        print(f"   ✅ Fetched!")
        print(f"   Repo      : {fetched['repo']}")
        print(f"   PR Number : {fetched['pr_number']}")
        print(f"   PR Title  : {fetched['pr_title']}")
        print(f"   Score     : {fetched['review']['quality_score']}/10")
        print(f"   Saved at  : {fetched['created_at']}\n")
    else:
        print("   ❌ Could not fetch review\n")

    # Test 3: Get all reviews
    print("🧪 Test 3: Getting all reviews...")
    all_reviews = get_all_reviews()
    print(f"   ✅ Total reviews in database: {len(all_reviews)}\n")

    # Test 4: Delete the review
    print("🧪 Test 4: Deleting the review...")
    deleted = delete_review(record_id)
    if deleted:
        print(f"   ✅ Review #{record_id} deleted\n")
    else:
        print(f"   ❌ Could not delete review\n")

    print("=" * 52)
    print("  ✅ Day 2 Complete — Database is working!")
    print("=" * 52)
    print()
    print("  reviews.db file created in your project folder")
    print("  Next → Day 3: Create backend/api.py")
    print()
