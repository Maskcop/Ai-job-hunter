import json


def load_jobs():

    with open(
        "jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def normalize_skill(skill):

    return skill.lower().strip()


def calculate_match(
    candidate_skills,
    job
):

    candidate_skills = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    required_skills = {
        normalize_skill(skill)
        for skill in job["required_skills"]
    }

    preferred_skills = {
        normalize_skill(skill)
        for skill in job["preferred_skills"]
    }


    # --------------------------------
    # Required skill matching
    # --------------------------------

    required_matches = (
        candidate_skills &
        required_skills
    )


    # --------------------------------
    # Missing required skills
    # --------------------------------

    missing_required = (
        required_skills -
        candidate_skills
    )


    # --------------------------------
    # Preferred skill matching
    # --------------------------------

    preferred_matches = (
        candidate_skills &
        preferred_skills
    )


    # --------------------------------
    # Match reasons
    # --------------------------------

    match_reasons = []

    for skill in sorted(required_matches):

        match_reasons.append(
            f"Strong match in {skill}"
        )


    # --------------------------------
    # Gap reasons
    # --------------------------------

    gap_reasons = []

    for skill in sorted(missing_required):

        gap_reasons.append(
            f"Missing required skill: {skill}"
        )


    # --------------------------------
    # Calculate scores
    # --------------------------------

    required_score = (
        len(required_matches)
        / len(required_skills)
        * 80
        if required_skills
        else 0
    )


    preferred_score = (
        len(preferred_matches)
        / len(preferred_skills)
        * 20
        if preferred_skills
        else 0
    )


    score = round(
        required_score +
        preferred_score
    )


    # --------------------------------
    # Return result
    # --------------------------------

    return {

        "job_id": job["id"],

        "title": job["title"],

        "company": job["company"],

        "location": job["location"],

        "match_score": score,

        "matching_skills": sorted(
            required_matches |
            preferred_matches
        ),

        "missing_skills": sorted(
            missing_required
        ),

        "match_reasons": match_reasons,

        "gap_reasons": gap_reasons

    }


def rank_jobs(candidate_skills):

    jobs = load_jobs()

    results = []


    for job in jobs:

        result = calculate_match(
            candidate_skills,
            job
        )

        results.append(result)


    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )


    return results