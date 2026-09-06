from job_recommendation import recommend_jobs


resume = """
Full Stack Developer with experience in
React.js, JavaScript, Node.js, Express.js,
SQL, MongoDB, Git, GitHub and REST APIs.

Built web applications and backend REST APIs.
"""


result = recommend_jobs(
    resume
)


print("\n==============================")
print("CANDIDATE SKILLS")
print("==============================")

for skill in result["candidate_skills"]:
    print("✓", skill)


print("\n==============================")
print("RECOMMENDED JOBS")
print("==============================")


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
        f"Matching: {job['matching_skills']}"
    )

    print(
        f"Missing: {job['missing_skills']}"
    )