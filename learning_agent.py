import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel


# --------------------------------------------------
# API KEY
# --------------------------------------------------

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")


# --------------------------------------------------
# GEMINI
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key
)


# --------------------------------------------------
# STRUCTURED OUTPUT
# --------------------------------------------------

class LearningPlan(BaseModel):
    skill: str
    priority: str
    why_learn: str
    topics: List[str]
    practice_task: str
    mini_project: str


class LearningPlans(BaseModel):
    plans: List[LearningPlan]


learning_llm = llm.with_structured_output(
    LearningPlans
)


# --------------------------------------------------
# PROMPT
# --------------------------------------------------

prompt = ChatPromptTemplate.from_template("""
You are an expert technical career mentor.

Create a personalized learning plan for ALL missing
skills at once.

Candidate's existing skills:
{matching_skills}

Missing skills:
{missing_skills}

Create one learning plan for every missing skill.

Rules:

1. Cover EVERY missing skill.
2. Do NOT create separate plans through separate AI calls.
3. Keep each plan practical.
4. Explain why the candidate should learn the skill.
5. Give the most important topics in order.
6. Give one practice task.
7. Give one mini project.
8. Do not invent candidate experience.
9. Focus on the target job.

Return one structured response containing all plans.
""")


# --------------------------------------------------
# ONE LEARNING AGENT CALL
# --------------------------------------------------

def create_learning_plans(
    matching_skills,
    missing_skills
):

    messages = prompt.invoke({
        "matching_skills": ", ".join(matching_skills),
        "missing_skills": str(missing_skills)
    })

    response = learning_llm.invoke(messages)

    return response.plans