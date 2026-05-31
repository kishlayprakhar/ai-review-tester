"""
==============================================
  AI Code Reviewer — backend/api.py
  Week 3, Day 3: FastAPI Server
==============================================

HOW TO RUN
    cd "D:\my project"
    uvicorn backend.api:app --reload
 

THEN OPEN:
    http://localhost:8000          → health check
    http://localhost:8000/docs     → interactive API docs
    http://localhost:8000/prs      → list PRs
    http://localhost:8000/review   → get AI review
    http://localhost:8000/history  → past reviews

ENDPOINTS:
    GET  /           → health check
    GET  /prs        → list open PRs for a repo
    POST /review     → get AI review for a PR
    GET  /history    → get all past reviews
    DELETE /review/{id} → delete a review
"""

# ── Imports ───────────────────────────────────────────────────────────────────

import sys
import os

# Make sure Python finds all backend files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi             import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic            import BaseModel
from typing              import Optional

from github_utils        import get_pull_requests, get_pr_diff
from claude_utils        import get_code_review
from database            import save_review, get_review, get_all_reviews, delete_review
from github import Github

# ── FastAPI App ───────────────────────────────────────────────────────────────

app = FastAPI(
    title       = "AI Code Reviewer",
    description = "Automatically review GitHub PRs using Groq AI",
    version     = "1.0.0"
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
gh_client = Github(GITHUB_TOKEN)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any frontend (like your React port 3000) to connect
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all custom HTTP headers
)

# ── CORS Middleware ───────────────────────────────────────────────────────────
# Allows frontend (React/HTML on port 3000) to talk to this server (port 8000)
# Without this the browser would block the requests

app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],    # allow all origins in development
    allow_methods  = ["*"],    # allow GET, POST, DELETE etc.
    allow_headers  = ["*"]     # allow all headers
)


# ── Request Models (Pydantic) ─────────────────────────────────────────────────
# These define what data each endpoint expects
# FastAPI validates automatically — if data is wrong it returns 422 error

class ReviewRequest(BaseModel):
    """Request body for POST /review"""
    repo      : str            # e.g. "psf/requests"
    pr_number : int            # e.g. 1234

class PRListRequest(BaseModel):
    """Query for listing PRs"""
    repo  : str                # e.g. "psf/requests"
    state : Optional[str] = "open"   # "open", "closed", or "all"
    limit : Optional[int] = 5        # max number of PRs to return


# ── Endpoint 1 — Health Check ─────────────────────────────────────────────────

@app.get("/")
def health_check():
    """
    Check if the server is running.
    Open http://localhost:8000 in browser to test.
    """
    return {
        "status"  : "running",
        "message" : "AI Code Reviewer API is live!",
        "version" : "1.0.0",
        "docs"    : "http://localhost:8000/docs"
    }


# ── Endpoint 2 — List Pull Requests ──────────────────────────────────────────

@app.get("/prs")
def list_prs(repo: str, state: str = "open", limit: int = 5):
    """
    List open Pull Requests for a GitHub repository.

    Query params:
        repo  : GitHub repo e.g. psf/requests
        state : open / closed / all (default: open)
        limit : max PRs to return (default: 5)

    Example:
        GET http://localhost:8000/prs?repo=psf/requests
    """
    print(f"\n📋 Fetching PRs for {repo}...")

    try:
        prs = get_pull_requests(repo, state=state, limit=limit)

        if not prs:
            raise HTTPException(
                status_code = 404,
                detail      = f"No {state} PRs found in {repo}"
            )

        return prs

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail      = f"Could not fetch PRs: {str(e)}"
        )


# ── Endpoint 3 — Review a PR ──────────────────────────────────────────────────

@app.post("/review")
def review_pr(request: ReviewRequest):
    try:
        # Connect to the specified GitHub repository and pull request
        repo = gh_client.get_repo(request.repo)
        pr = repo.get_pull(request.pr_number)

      
        # -----------------------------------------------------------------
        pr_files = pr.get_files()
        detected_languages = set()
        raw_diff_content = ""
        
        for file in pr_files:
            if file.patch:
                raw_diff_content += f"\nFile: {file.filename}\n{file.patch}\n"
                
                # Check extensions dynamically
                ext = file.filename.split('.')[-1].lower()
                if ext == 'py': detected_languages.add("Python")
                elif ext in ['js', 'jsx', 'ts', 'tsx']: detected_languages.add("JavaScript/TypeScript")
                elif ext in ['c', 'cpp', 'h']: detected_languages.add("C/C++")
                elif ext == 'java': detected_languages.add("Java")
                elif ext == 'go': detected_languages.add("Go")

        languages_context = ", ".join(detected_languages) if detected_languages else "General Source Code"
        print(f"🌐 Dynamic Language Detection complete. Found: {languages_context}")

        
        # Extract the latest commit object (Strictly required by GitHub for line-level comments)
        commits = pr.get_commits()
        latest_commit = commits[commits.totalCount - 1]
        
        # Gather information about changed files
        pr_files = pr.get_files()
        
        # Define mock structured data matching your frontend parser expectations
        structured_review = {
            "bugs": [
                "Potential circular reference detected. Refactor to merge common utility functions.",
                "Error handler does not catch ConnectionRefusedError. Update exception fallback types."
            ],
            "improvements": [
                {"description": "Replace list comprehension with a generator expression to optimize loop memory usage."},
                {"description": "Cache responses from the GitHub API using st.cache_data mechanism structures."}
            ],
            "security_issues": [
                "Identified use of a deprecated hashing algorithm SHA1 in database configuration arrays."
            ],
            "quality_score": 9,
            "summary": "Overall changes are well-structured and significantly improve script robustness parameters."
        }

        # -----------------------------------------------------------------
        # ADVANCED FEATURE 1: Auto-Post Global PR Review Comment
        # -----------------------------------------------------------------
        global_markdown_comment = f"""### 🤖 Automated AI Code Review
| Metric | Status / Value |
| :--- | :--- |
| **⭐ Quality Score** | **{structured_review['quality_score']}/10** |

#### 🪲 Bugs Identified
- {structured_review['bugs'][0]}
- {structured_review['bugs'][1]}

#### ⚡ Performance Modifications
- {structured_review['improvements'][0]['description']}

#### 🔒 Security Scans
- {structured_review['security_issues'][0]}

*Review generated successfully via Full-Stack Application Integration Pipelines.*"""

        try:
            # Post the global overview comment to the PR timeline
            pr.create_issue_comment(global_markdown_comment)
            print("✅ Successfully posted global overview review comment to GitHub!")
        except Exception as github_err:
            print(f"⚠️ Global comment posting bypassed: {str(github_err)} (Check token write permissions)")

        # -----------------------------------------------------------------
        # ADVANCED FEATURE 2: Line-Level Diff Target Comments Pinning
        # -----------------------------------------------------------------
        # Iterate through the files modified in the PR to find a place to pin comments
        for file in pr_files:
            # If the PR contains any Python files, let's pin an actionable issue onto the diff patch
            if file.filename.endswith(".py") and file.patch:
                try:
                    # We look at line position 1 of the file's modifications diff patch
                    pr.create_review_comment(
                        body="💡 **AI Inline Suggestion:** Verify this code layer is decoupled safely to maximize microservice scaling speeds.",
                        commit=latest_commit,
                        path=file.filename,
                        position=1 # Pinned dynamically at line position 1 inside the git patch sequence block
                    )
                    print(f"📌 Inline code suggestion successfully pinned to file: {file.filename}")
                    break # Stop after pinning one code comment for validation testing
                except Exception as line_err:
                    print(f"⚠️ Inline comment bypassed on {file.filename}: {str(line_err)}")

        # Return structured response payload straight to your Streamlit user interface grid elements
        return {
            "status": "success",
            "review": structured_review
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advanced Features Execution Failure: {str(e)}")


# ── Endpoint 4 — Get Review History ──────────────────────────────────────────

@app.get("/history")
def get_history():
    """
    Get all past AI reviews from the database.
    Most recent first.

    Example:
        GET http://localhost:8000/history
    """
    print("\n📚 Fetching review history...")

    reviews = get_all_reviews()

    return {
        "count"   : len(reviews),
        "reviews" : reviews
    }


# ── Endpoint 5 — Get Single Review ───────────────────────────────────────────

@app.get("/review/{repo:path}/{pr_number}")
def get_single_review(repo: str, pr_number: int):
    """
    Get a specific saved review by repo and PR number.

    Example:
        GET http://localhost:8000/review/psf/requests/1234
    """
    review = get_review(repo, pr_number)

    if not review:
        raise HTTPException(
            status_code = 404,
            detail      = f"No saved review found for PR #{pr_number} in {repo}"
        )

    return review


# ── Endpoint 6 — Delete Review ───────────────────────────────────────────────

@app.delete("/review/{review_id}")
def delete_review_by_id(review_id: int):
    """
    Delete a review by its database ID.

    Example:
        DELETE http://localhost:8000/review/1
    """
    deleted = delete_review(review_id)

    if not deleted:
        raise HTTPException(
            status_code = 404,
            detail      = f"Review #{review_id} not found"
        )

    return {
        "message"   : f"Review #{review_id} deleted successfully",
        "review_id" : review_id
    }




@app.post("/review")
def review_pr(request: ReviewRequest):
    try:
        diff = get_pr_diff(request.repo, request.pr_number)

        if not diff:
            raise HTTPException(
                status_code=404,
                detail=f"PR #{request.pr_number} not found in {request.repo}"
            )

        review = get_code_review(diff)
        return review

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))