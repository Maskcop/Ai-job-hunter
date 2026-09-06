from job_ai_analysis import (
    analyze_job_with_ai
)


resume = """
Full Stack Developer with experience
in React.js, JavaScript, Python,
FastAPI, SQL, Git and REST APIs.
"""


job_description = """
Looking for a Full Stack Developer
with React, Python, FastAPI, SQL,
Docker and AWS experience.
"""


result = analyze_job_with_ai(

    resume=resume,

    job_description=
        job_description,

    match_score=80,

    matching_skills=[
        "React",
        "Python",
        "FastAPI",
        "SQL"
    ],

    missing_skills=[
        "Docker",
        "AWS"
    ]
)


print("\n==============================")
print("AI JOB ANALYSIS")
print("==============================")

print(result)