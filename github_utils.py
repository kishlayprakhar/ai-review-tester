from github import Github
from dotenv import load_dotenv
import os
from groq import Groq
import json

# Load environment variables from .env file
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
gh_client = Github(GITHUB_TOKEN)

def get_github_client():
    """Create and return an authenticated GitHub client"""
    return Github(GITHUB_TOKEN)

def get_repo(repo_name):
    """
    Fetch a GitHub repository object
    repo_name format: "username/repository-name"
    Example: "torvalds/linux"
    """
    client = get_github_client()
    repo = client.get_repo(repo_name)
    print(f"✅ Connected to repo: {repo.full_name}")
    print(f"   Description: {repo.description}")
    print(f"   Stars: {repo.stargazers_count}")
    return repo

# Test it
if __name__ == "__main__":
    repo = get_repo("facebook/react")  # test with any public repo

def get_pull_requests(repo_name, state="open", limit=5):
    """
    Fetch pull requests from a repository
    
    state: "open", "closed", or "all"
    limit: how many PRs to fetch
    """
    repo = get_repo(repo_name)
    pull_requests = repo.get_pulls(state=state, sort="created", direction="desc")
    
    pr_list = []
    print(f"\n📋 Fetching {limit} {state} PRs from {repo_name}:\n")
    
    for i, pr in enumerate(pull_requests):
        if i >= limit:
            break
            
        pr_info = {
            "number": pr.number,
            "title": pr.title,
            "author": pr.user.login,
            "created_at": str(pr.created_at),
            "url": pr.html_url
        }
        pr_list.append(pr_info)
        
        print(f"  PR #{pr.number}: {pr.title}")
        print(f"  Author: {pr.user.login}")
        print(f"  URL: {pr.html_url}")
        print(f"  ---")
    
    return pr_list

# Test it
if __name__ == "__main__":
    get_pull_requests("microsoft/vscode", state="open", limit=3)


def get_pr_diff(repo_name, pr_number):
    """
    Fetch the full diff of a specific Pull Request
    
    Returns a list of changed files with their diffs
    """
    repo = get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    print(f"\n🔍 Fetching diff for PR #{pr_number}: {pr.title}")
    print(f"   Files changed: {pr.changed_files}")
    print(f"   Lines added: {pr.additions}")
    print(f"   Lines removed: {pr.deletions}\n")
    
    files_data = []
    
    for file in pr.get_files():
        file_info = {
            "filename": file.filename,
            "status": file.status,        # added, modified, removed
            "additions": file.additions,
            "deletions": file.deletions,
            "patch": file.patch            # This is the actual diff!
        }
        files_data.append(file_info)
        
        print(f"  📄 File: {file.filename}")
        print(f"     Status: {file.status}")
        print(f"     +{file.additions} additions, -{file.deletions} deletions")
        print(f"\n     Diff preview:")
        
        # Print first 20 lines of diff as preview
        if file.patch:
            diff_lines = file.patch.split('\n')[:20]
            for line in diff_lines:
                if line.startswith('+'):
                    print(f"     🟢 {line}")   # Added lines
                elif line.startswith('-'):
                    print(f"     🔴 {line}")   # Removed lines
                else:
                    print(f"        {line}")   # Context lines
        print()
    
    return files_data



def analyze_and_post_gh_review(repo_name: str, pr_number: int, ai_client):
    """
    Handles the entire Advanced Week 5 flow:
    1. Language Detection
    2. Severity Label enforcement via AI prompt engineering
    3. Auto-posting the final review back to the GitHub PR as a comment
    """
    repo = GITHUB_TOKEN.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # ---------------------------------------------
    # FEATURE 1: Language Detection
    # ---------------------------------------------
    detected_languages = set()
    pr_files = pr.get_files()
    
    for file in pr_files:
        ext = file.filename.split('.')[-1].lower()
        if ext == 'py': detected_languages.add('Python')
        elif ext in ['js', 'jsx', 'ts', 'tsx']: detected_languages.add('JavaScript/TypeScript')
        elif ext == 'java': detected_languages.add('Java')
        elif ext == 'cpp' or ext == 'c': detected_languages.add('C/C++')

    lang_context = ", ".join(detected_languages) if detected_languages else "General Source Code"
    print(f"🌐 Detected Languages in PR: {lang_context}")

    # ---------------------------------------------
    # FEATURE 2: Severity Labels Prompt Design
    # ---------------------------------------------
    # We explicitly instruct the AI to build responses with standardized tags
    system_prompt = f"""
    You are an expert elite code reviewer analyzing a pull request written in: {lang_context}.
    Tailor your feedback strictly to the best practices of these languages.
    
    CRITICAL COMPLIANCE: You must categorize every issue you find into one of these strict severity labels:
    - [CRITICAL]: For severe security vulnerabilities, crashes, or catastrophic broken logic.
    - [WARNING]: For performance bottlenecks, code smells, or moderate issues.
    - [INFO]: For stylistic upgrades, micro-optimizations, or clean-up suggestions.
    
    Format your final response cleanly with markdown sections separating Bugs, Performance, Security, and your final Score out of 10.
    """

    # --- (Simulated block: Grab your git diff and send it to Groq/Claude) ---
    # raw_diff = ""
    # for file in pr_files: raw_diff += f"File: {file.filename}\n{file.patch}\n"
    # ai_review_text = ai_client.generate(system_prompt, raw_diff)
    
    # For demonstration, let's assume your AI successfully generated a response containing the tags:
    ai_review_text = f"""
    ### 🐛 Bugs Found
    - [WARNING] Missing a try-except fallback block in your database pool script.
    
    ### ⚡ Performance Suggestions
    - [INFO] Consider replacing the loops with list comprehensions for speed.
    
    ### 🔒 Security Issues
    - [CRITICAL] Hardcoded test credentials detected on line 12. Remove immediately!
    
    ### ⭐ Quality Score
    7.5/10
    """

    # ---------------------------------------------
    # FEATURE 3: Auto-Post review as a GitHub PR Comment
    # ---------------------------------------------
    comment_header = f"### 🤖 Automated AI Code Review v2.0\n*Tailored for: {lang_context}*\n\n"
    full_github_comment = comment_header + ai_review_text
    
    # This automatically writes the comment onto the live GitHub PR page!
    pr.create_review_comment(full_github_comment)
    print(f"✅ Successfully auto-posted review comment to {repo_name} PR #{pr_number}!")

    return ai_review_text



# Add this at the bottom of backend/github_utils.py

def post_line_level_comment(pr, file_path, commit_object, line_number_in_diff, comment_body):
    """
    Pins an AI code suggestion directly onto a specific line of code 
    inside a specific file on the active GitHub Pull Request.
    """
    try:
        pr.create_review_comment(
            body=comment_body,
            commit=commit_object,        # The target commit object
            path=file_path,              # e.g., "backend/api.py"
            position=line_number_in_diff  # The exact line relative to the git patch diff
        )
        print(f"📌 Pinned line-level comment on {file_path} at line position {line_number_in_diff}")
    except Exception as e:
        print(f"⚠️ Failed to post line-level comment: {str(e)}")