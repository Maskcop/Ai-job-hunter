import os
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List


api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key
)


class InterviewQuestion(BaseModel):
    question: str
    skill: str
    difficulty: str
    reason: str


class InterviewQuestions(BaseModel):
    questions: List[InterviewQuestion]


structured_llm = llm.with_structured_output(
    InterviewQuestions
)


prompt = ChatPromptTemplate.from_template("""
You are a senior technical interviewer.

Create interview questions for a candidate based on the
candidate's skills and skill gaps.

Matching skills:
{matching_skills}

Missing skills:
{missing_skills}

Learning plans:
{learning_plans}

Create 5 technical interview questions.

Rules:
1. Questions must be relevant to the candidate's skills.
2. Include questions about their strong skills.
3. Include questions about important missing skills.
4. Mix easy, medium and hard questions.
5. Explain why each question is relevant.
6. Do not invent candidate experience.
""")


def generate_interview_questions(
    matching_skills,
    missing_skills,
    learning_plans
):

    messages = prompt.invoke({
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "learning_plans": learning_plans
    })

    response = structured_llm.invoke(messages)

    return response.questions