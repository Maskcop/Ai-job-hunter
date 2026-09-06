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


class ResumeSuggestions(BaseModel):
    suggestions: List[str]


structured_llm = llm.with_structured_output(
    ResumeSuggestions
)


prompt = ChatPromptTemplate.from_template("""
You are an expert technical resume reviewer.

The candidate has a low match score for a job.

Matching skills:
{matching_skills}

Missing skills:
{missing_skills}

Create resume improvement suggestions.

Rules:

1. Suggest improvements based only on the information provided.
2. Never invent skills or experience.
3. Do not tell the candidate to add a skill they do not have.
4. Focus on making existing experience clearer.
5. Give 5 practical suggestions.
""")


def optimize_resume(
    matching_skills,
    missing_skills
):

    messages = prompt.invoke({
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    })

    response = structured_llm.invoke(messages)

    return response.suggestions