# 🤖 Automated AI Code Review Dashboard

A full-stack, AI-powered code review assistant that connects to the GitHub REST API to automatically analyze pull requests, calculate a quality score, flag security issues, and auto-post reviews and line-level comments back to GitHub.

## 🚀 Live Demo
* **Frontend Dashboard:** [Paste your Streamlit Cloud URL here]
* **Backend API:** [Paste your Render Service URL here]

## 🛠️ Tech Stack
* **Frontend:** Streamlit, Altair (Data Visualization)
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Integrations:** PyGithub (GitHub REST API), Groq / Google Gemini API

## 📋 Features Completed (Week 5 & 6)
- [x] **Auto-Post PR Comments:** Automatically drops a markdown summary matrix into the PR timeline.
- [x] **Line-Level Comments:** Pins actionable optimization suggestions to specific lines inside the git diff patch.
- [x] **Dynamic Language Detection:** Automatically adapts system prompt contexts based on file extensions (.py, .js, .c).
- [x] **Severity Labels:** Tags scanned bugs with `[CRITICAL]`, `[WARNING]`, or `[INFO]` markers.
- [x] **Cloud Deployment:** Production backend hosted on Render; frontend interface running on Streamlit Cloud.

## 🔧 Local Setup Instructions
1. Clone the repository:
   ```bash
   git clone [https://github.com/kishlayprakhar/ai-review-tester.git](https://github.com/kishlayprakhar/ai-review-tester.git)
