from github_utils import get_pull_requests, get_pr_diff
import json
import sys
import os
from display_utils import display_review
from claude_utils  import get_code_review
from pydantic import BaseModel


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
 

 


 


def analyze_repo(repo_name):
    """
    Runs the full pipeline from GitHub PR to AI review.
 
    Parameters:
        repo_name (str): GitHub repo in "username/repo" format
                         Example: "psf/requests"
    """
 
    print()
    print("=" * 55)
    print("  🚀 AI Code Reviewer — Powered by Groq")
    print(f"  📦 Repo : {repo_name}")
    print("=" * 55)
    print()
 

    print("📋 Step 1: Fetching open Pull Requests...\n")
 
    prs = get_pull_requests(repo_name, state="open", limit=5)
 
    if not prs:
        print("❌ No open PRs found in this repo.")
        print("   Try a repo with open PRs or change state to 'closed'")
        return
 
    print(f"\n   Found {len(prs)} open PR(s)\n")
 

    first_pr = prs[0]
 
    print(f"📥 Step 2: Getting diff for PR #{first_pr['number']}...")
    print(f"   Title : {first_pr['title']}")
    print(f"   Author: {first_pr['author']}")
    print(f"   URL   : {first_pr['url']}\n")
 
    diff_data = get_pr_diff(repo_name, first_pr["number"])
 
    if not diff_data:
        print("❌ Could not fetch diff for this PR.")
        print("   The PR may have no code changes.")
        return
 
    print(f"\n   Total files changed: {len(diff_data)}\n")
 
 
    print("🤖 Step 3: Sending diff to Groq for AI review...\n")
 
    review = get_code_review(diff_data)
 
    if not review:
        print("❌ Could not get a review from Groq.")
        print("   Check your GROQ_API_KEY in .env")
        return
 
  
    print("📊 Step 4: Displaying Review...\n")
 
    display_review(review, pr_title=first_pr["title"])
 
   
    output = {
        "pr_number" : first_pr["number"],
        "pr_title"  : first_pr["title"],
        "pr_author" : first_pr["author"],
        "pr_url"    : first_pr["url"],
        "repo"      : repo_name,
        "review"    : review
    }
 
    # Save to root folder (one level above backend/)
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "review_output.json"
    )
 
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
 
    print(f"💾 Step 5: Full review saved to review_output.json")
 
    print()
    print("=" * 55)
    print("  ✅ Week 2 Complete!")
    print("  Next → Week 3: Build the FastAPI backend")
    print("=" * 55)
    print()
 
 
 
#if __name__ == "__main__":

    #analyze_repo("psf/requests")
 



class ReviewRequest(BaseModel):
    repo      : str
    pr_number : int

