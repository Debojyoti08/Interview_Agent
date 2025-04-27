from fastapi import FastAPI, Request
import json
import os
from datetime import datetime
from backend import gemini_service

app = FastAPI()

# Path to store interview sessions
DATA_FILE = "interview_sessions.json"

# Helper to load existing data
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Helper to save updated data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Initialize session storage
session_answers = load_data()

@app.post("/process-answer")
async def process_answer(req: Request):
    body = await req.json()
    user_id = body.get('user_id', 'unknown_user')  # You can replace this with real user_id
    user_text = body.get('transcript', '')

    # Initialize user session if not exists
    if user_id not in session_answers:
        session_answers[user_id] = {
            "job_role": body.get('job_role', 'Unknown Role'),
            "start_time": str(datetime.now()),
            "answers": []
        }

    # Save the answer
    session_answers[user_id]["answers"].append({
        "timestamp": str(datetime.now()),
        "text": user_text
    })

    # Save the updated session to JSON file
    save_data(session_answers)

    # Check if user said "end interview"
    if "end interview" in user_text.lower() or "stop" in user_text.lower():
        # Analyze all collected answers
        all_answers = [a["text"] for a in session_answers[user_id]["answers"]]
        final_feedback = gemini_service.analyze_answers(all_answers)

        return {
            "action": "speak_text",
            "text": f"Thank you for completing the interview. Here's your feedback: {final_feedback}",
            "next": "end_call"
        }
    
    # Otherwise, generate next question
    next_question = gemini_service.generate_question(session_answers[user_id]["job_role"])

    return {
        "question": next_question
    }
