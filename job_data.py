import json


def load_jobs():

    with open(
        "jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def search_jobs(
    keyword=None,
    location=None
):

    jobs = load_jobs()

    results = []

    for job in jobs:

        if keyword:

            text = (
                job["title"] +
                " " +
                job["description"]
            ).lower()

            if keyword.lower() not in text:
                continue


        if location:

            if (
                location.lower()
                not in job["location"].lower()
            ):
                continue


        results.append(job)


    return results