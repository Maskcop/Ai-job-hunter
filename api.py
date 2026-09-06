from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import PyPDFLoader

import tempfile
import os

from career_service import run_career_analysis
from rag_pipeline import analyze_resume
from job_recommendation import recommend_jobs
from ats_analyzer import analyze_ats


app = FastAPI(
    title="AI Job Hunter",
    version="1.0"
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# HOME
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "AI Job Hunter API is running 🚀"
    }


# =========================================================
# ANALYZE RESUME AGAINST JOB DESCRIPTION
# =========================================================

@app.post("/analyze")
async def analyze_resume_api(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Create temporary PDF file
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            await resume.read()
        )

        pdf_path = temp_file.name

    try:

        # ---------------------------------
        # 1. Load Resume PDF
        # ---------------------------------

        loader = PyPDFLoader(pdf_path)

        documents = loader.load()


        # ---------------------------------
        # 2. Extract Resume Text
        # ---------------------------------

        resume_text = "\n\n".join(
            doc.page_content
            for doc in documents
        )


        # ---------------------------------
        # 3. Resume + JD Analysis
        # ---------------------------------

        analysis = analyze_resume(
            resume_documents=documents,
            job_description=job_description
        )


        # ---------------------------------
        # 4. ATS Analysis
        # ---------------------------------

        ats_result = analyze_ats(
            resume_text=resume_text,
            job_description=job_description
        )


        # ---------------------------------
        # 5. Career AI
        # ---------------------------------

        career_result = run_career_analysis(
            analysis
        )


        # ---------------------------------
        # 6. Return Everything
        # ---------------------------------

        return {

            "resume_filename": resume.filename,


            # =============================
            # JOB MATCH ANALYSIS
            # =============================

            "job_analysis": {

                "match_score": analysis.match_score,

                "matching_skills": [
                    {
                        "skill": item.skill,
                        "resume_evidence": item.resume_evidence,
                        "job_requirement": item.job_requirement
                    }

                    for item in analysis.matching_skills
                ],


                "missing_skills": [
                    {
                        "skill": item.skill,
                        "priority": item.priority,
                        "reason": item.reason
                    }

                    for item in analysis.missing_skills
                ],


                "experience_match": analysis.experience_match,

                "recommendation": analysis.recommendation
            },


            # =============================
            # ATS ANALYSIS
            # =============================

            "ats_analysis": ats_result.model_dump(),


            # =============================
            # CAREER AI
            # =============================

            "career_analysis": career_result

        }


    finally:

        # Delete temporary PDF
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


# =========================================================
# RECOMMEND JOBS
# =========================================================

@app.post("/recommend-jobs")
async def recommend_jobs_api(
    resume: UploadFile = File(...),
    keyword: str = Form(None),
    location: str = Form(None)
):

    # Create temporary PDF
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            await resume.read()
        )

        pdf_path = temp_file.name


    try:

        # Load PDF
        loader = PyPDFLoader(pdf_path)

        documents = loader.load()


        # Extract resume text
        resume_text = "\n\n".join(
            doc.page_content
            for doc in documents
        )


        # Find recommended jobs
        result = recommend_jobs(
            resume_text=resume_text,
            keyword=keyword,
            location=location
        )


        return {

            "resume_filename": resume.filename,

            "search": {
                "keyword": keyword,
                "location": location
            },

            "recommendations": result

        }


    finally:

        # Delete temporary PDF
        if os.path.exists(pdf_path):
            os.remove(pdf_path)