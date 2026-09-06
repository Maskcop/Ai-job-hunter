import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


prompt = ChatPromptTemplate.from_template(
    """
You are an expert technical recruiter.

Analyze the candidate against the job.

Candidate Resume:
{resume}

Job Description:
{job_description}

Match Score:
{match_score}

Matching Skills:
{matching_skills}

Missing Skills:
{missing_skills}

Give a short and practical analysis.

Return:

Why You Match:
- 2 to 4 points

Main Skill Gaps:
- 1 to 4 points

Recommendation:
Choose one:
- Strongly Apply
- Apply
- Consider After Upskilling
- Not a Good Match

Reason:
One short explanation.

Use only information provided above.
"""
)


def analyze_job_with_ai(
    resume,
    job_description,
    match_score,
    matching_skills,
    missing_skills
):

    messages = prompt.invoke({

        "resume": resume,

        "job_description":
            job_description,

        "match_score":
            match_score,

        "matching_skills":
            ", ".join(
                matching_skills
            ),

        "missing_skills":
            ", ".join(
                missing_skills
            )

    })


    response = llm.invoke(
        messages
    )


    return response.content