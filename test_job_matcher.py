from job_matcher import rank_jobs


candidate_skills = [
    "Java",
    "React",
    "JavaScript",
    "SQL",
    "REST APIs",
    "Git"
]


results = rank_jobs(
    candidate_skills
)


print("\n🔥 JOB MATCHES\n")


for index, job in enumerate(
    results,
    start=1
):

    print(
        f"{index}. {job['title']}"
    )

    print(
        f"   Company: {job['company']}"
    )

    print(
        f"   Location: {job['location']}"
    )

    print(
        f"   Match: {job['match_score']}%"
    )

    print(
        f"   Matching: {job['matching_skills']}"
    )

    print(
        f"   Missing: {job['missing_skills']}"
    )

    print()