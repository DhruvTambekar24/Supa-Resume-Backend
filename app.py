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
    As a seasoned **HR Manager**, thoroughly evaluate the candidate's resume against the provided **job description**.
    Provide a **detailed analysis** of the candidate's suitability for the role by highlighting **key strengths**, **potential weaknesses**, and **areas for improvement**.
    Emphasize how well the candidate’s **experience**, **skills**, and **qualifications** align with the **job requirements**, using **bold formatting** for critical insights.
    """,
    
    "ats_match": """
    Act as an advanced **ATS (Applicant Tracking System)** scanner to assess the resume's **compatibility** with the given **job description**.
    Deliver a **precise percentage match**, identify **missing or underrepresented keywords**, and provide a **detailed analysis** of the resume's **overall alignment** with the job requirements.
    Include **actionable suggestions** to improve **ATS performance**, ensuring all important points are **bolded** for quick reference.
    """,
    
    "project_suggestions": """
    Take on the role of a dedicated **mentor** guiding the candidate to bridge **skill gaps** identified in the resume.
    Propose **2 impactful project ideas**, including **relevant data sources** and a **step-by-step deployment plan**.
    Provide **detailed insights** into each project, ensuring alignment with **industry trends** and emphasizing **key concepts** in **bold** to enhance clarity.
    """,
    
    "resume_improvement": """
    Provide **professional recommendations** to enhance the resume's **structure**, **format**, and **presentation**.
    Offer **specific formatting tips**, **layout suggestions**, and **examples** of effective resume sections.
    Share **detailed guidelines** to make the resume **polished**, **ATS-friendly**, and **tailored** for **maximum impact** in the candidate’s **target industry**, with important tips **bolded** for emphasis.
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
