from job_data import search_jobs


print("\n🔥 ALL JOBS\n")

jobs = search_jobs()

for job in jobs:

    print(
        job["title"],
        "-",
        job["company"]
    )


print("\n🔥 REACT JOBS\n")

jobs = search_jobs(
    keyword="React"
)

for job in jobs:

    print(
        job["title"],
        "-",
        job["company"]
    )


print("\n🔥 PUNE JOBS\n")

jobs = search_jobs(
    location="Pune"
)

for job in jobs:

    print(
        job["title"],
        "-",
        job["company"]
    )