import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def generate_question(job_role):
    prompt = f"Generate an interview question for the role: {job_role}"
    response = model.generate_content(prompt)
    return response.text

def analyze_answers(all_answers):
    combined = "\n".join(all_answers)
    prompt = f"Analyze these interview answers:\n{combined}\nGive overall feedback, strengths, and areas to improve."
    response = model.generate_content(prompt)
    return response.text
