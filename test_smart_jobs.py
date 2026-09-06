from job_recommendation import recommend_jobs


resume = """
Full Stack Developer with experience in
React.js, JavaScript, Python, FastAPI,
SQL, PostgreSQL, Git and REST APIs.
"""


print("\n🔥 SEARCH: React + Pune\n")


result = recommend_jobs(
    resume_text=resume,
    keyword="React",
    location="Pune"
)


print(
    "Candidate Skills:",
    result["candidate_skills"]
)

print(
    "Total Jobs:",
    result["total_jobs"]
)


for index, job in enumerate(
    result["jobs"],
    start=1
):

    print(
        f"\n#{index} {job['title']}"
    )

    print(
        f"Company: {job['company']}"
    )

    print(
        f"Location: {job['location']}"
    )

    print(
        f"Match: {job['match_score']}%"
    )

    print(
        "Matching Skills:",
        job["matching_skills"]
    )

    print(
        "Missing Skills:",
        job["missing_skills"]
    )