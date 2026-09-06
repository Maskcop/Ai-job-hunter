import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key
)


class ATSKeyword(BaseModel):
    keyword: str
    importance: str
    found: bool


class ATSAnalysis(BaseModel):
    ats_score: int

    keyword_match_percentage: int

    matched_keywords: List[ATSKeyword]
    missing_keywords: List[ATSKeyword]

    formatting_issues: List[str]

    section_issues: List[str]

    improvement_suggestions: List[str]


structured_llm = llm.with_structured_output(ATSAnalysis)


prompt = ChatPromptTemplate.from_template("""
You are an expert ATS resume analyzer.

Analyze the candidate's resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}


Your task is to evaluate how well the resume is prepared
for this specific job.

Analyze:

1. ATS score from 0 to 100.

2. Keyword match percentage.

3. Identify important keywords from the job description.

4. For each important keyword determine whether it is
   genuinely supported by the resume.

5. Separate keywords into:
   - matched_keywords
   - missing_keywords

6. Assign importance:
   - HIGH
   - MEDIUM
   - LOW

7. Identify possible resume formatting issues that could
   hurt ATS parsing.

8. Identify missing or unclear resume sections.

9. Give practical improvement suggestions.

IMPORTANT RULES:

- NEVER invent experience.
- NEVER claim the candidate has a skill that is not supported
  by the resume.
- Do not recommend keyword stuffing.
- Missing keywords should only be recommended if the candidate
  genuinely has that skill.
- Focus specifically on this job description.
- Keep suggestions practical and honest.
""")


def analyze_ats(resume_text, job_description):

    messages = prompt.invoke({
        "resume_text": resume_text,
        "job_description": job_description
    })

    response = structured_llm.invoke(messages)

    return response