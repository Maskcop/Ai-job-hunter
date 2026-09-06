from semantic_matcher import calculate_similarity


resume = """
Full Stack Developer with experience
in React, JavaScript, Python, FastAPI,
SQL, PostgreSQL and REST APIs.
"""


job = """
We are looking for a Full Stack Developer
who can build web applications using React,
Python, FastAPI, SQL and REST APIs.
"""


score = calculate_similarity(
    resume,
    job
)


print(
    f"\nSemantic Match Score: {score}%"
)