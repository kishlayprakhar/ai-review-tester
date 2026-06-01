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
    print(f"\n🚀 Running dynamic AI review for {request.repo} PR #{request.pr_number}...")
    try:
        # 1. Fetch the actual code modifications (git diff patch)
        diff = get_pr_diff(request.repo, request.pr_number)

        if not diff:
            raise HTTPException(
                status_code=404,
                detail=f"PR #{request.pr_number} diff content not found in {request.repo}"
            )

        # 2. Fire the code diff to your dynamic AI model parser
        structured_review = get_code_review(diff)

        # 3. Pull out the variables for GitHub posting or fallback seamlessly
        quality_score = structured_review.get("quality_score", 7)
        summary_text = structured_review.get("summary", "Review processed.")
        bugs_array = structured_review.get("bugs", [])
        improvements_array = structured_review.get("improvements", [])
        security_array = structured_review.get("security_issues", [])

        # 4. Connect to GitHub Client for Auto-Posting Features
        try:
            repo = gh_client.get_repo(request.repo)
            pr = repo.get_pull(request.pr_number)

            # Build markdown layout matrices dynamically from actual AI content arrays
            bugs_md = "\n".join([f"- {b}" for b in bugs_array]) if bugs_array else "- No critical code bugs spotted."
            sec_md = "\n".join([f"- {s}" for s in security_array]) if security_array else "- No obvious data exposures found."
            
            global_markdown_comment = f"""### 🤖 Automated AI Code Review
| Metric | Status / Value |
| :--- | :--- |
| **⭐ Quality Score** | **{quality_score}/10** |

#### 🪲 Structural Bug Diagnostics
{bugs_md}

#### 🔒 Data Protection & Security
{sec_md}

*Review generated dynamically using live cloud access processing pipelines.*"""

            pr.create_issue_comment(global_markdown_comment)
            print("✅ Successfully posted live dynamic review overview comment to GitHub!")
            
            # Optional: Attempt line-level suggestions if patches exist
            commits = pr.get_commits()
            latest_commit = commits[commits.totalCount - 1]
            for file in pr.get_files():
                if file.filename.endswith(".py") and file.patch:
                    pr.create_review_comment(
                        body="💡 **AI Inline Suggestion:** Review execution layout optimization paths for this specific file block.",
                        commit=latest_commit,
                        path=file.filename,
                        position=1
                    )
                    break
        except Exception as github_err:
            print(f"⚠️ GitHub automated timeline integration bypassed: {str(github_err)}")

        # 5. Save the real review to history database log files
        try:
            save_review(
                repo=request.repo,
                pr_number=request.pr_number,
                pr_title=getattr(pr, 'title', f"PR #{request.pr_number}"),
                pr_author=getattr(getattr(pr, 'user', None), 'login', 'Unknown'),
                pr_url=f"https://github.com/{request.repo}/pull/{request.pr_number}",
                review=structured_review
            )
        except Exception as db_err:
            print(f"⚠️ History tracking database pass bypassed: {str(db_err)}")

        # 6. Return dynamic AI payload directly back to your Streamlit user interface
        return {
            "status": "success",
            "review": structured_review
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Pipeline Engine Error: {str(e)}")

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
