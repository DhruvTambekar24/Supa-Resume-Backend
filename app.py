from fastapi import FastAPI, File, UploadFile, Form
import google.generativeai as genai
from pypdf import PdfReader
from fastapi.middleware.cors import CORSMiddleware
import io

# Initialize Gemini API (Replace YOUR_API_KEY)
genai.configure(api_key="AIzaSyDed2gvIy3cb7GHeYrh-ZyrmNKEG5DcYJg")

app = FastAPI()

# CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read PDF
def read_pdf(file: UploadFile):
    pdf_reader = PdfReader(io.BytesIO(file.file.read()))
    text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

# Prompt Templates
PROMPTS = {
    "resume_analysis": """
    You are an experienced HR Manager reviewing a resume for a given job description.
    Please provide an evaluation of whether the candidate is a good fit.
    Highlight strengths and weaknesses.
    """,
    "ats_match": """
    You are an ATS scanner checking resume compatibility for a job.
    Give a percentage match, missing keywords, and final thoughts.
    """,
    "project_suggestions": """
    You are a mentor suggesting projects to improve missing skills.
    Suggest 2 project ideas with data sources, ML models, and deployment steps.
    """,
    "resume_improvement": """
    Suggest structural improvements for the resume, including formatting tips and examples.
    """
}

# Endpoints
@app.post("/analyze_resume/")
async def analyze_resume(job_description: str = Form(...), file: UploadFile = File(...), prompt_type: str = Form(...)):
    resume_text = read_pdf(file)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"{PROMPTS[prompt_type]}\n\nJob Description: {job_description}\nResume: {resume_text}")
    
    return {"response": response.text}

# Run server: uvicorn main:app --reload
